import json
import time
import logging

from flask import Flask, request

from command import Command
from commandDAO import CommandDAO
from exception import NotFoundException

class Server:
  _commandDAO = None
  _server = None

  def _shutdownIfNotMoreCommands(self):
    if self._commandDAO.countPendings() == 0:
      self._shutdown()

  def _shutdown(self):
    logging.info("Server.shutdown(): Shutdown server")
    function = request.environ.get('werkzeug.server.shutdown')
    if function is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    function()

  def popCommand(self, clientId):
    logging.debug("Server.popCommand(%s)" % clientId)
    command = self._commandDAO.findNextFromClient(clientId)
    if command is None: 
      raise NotFoundException()
    command.startTime = time.time()
    self._commandDAO.save(command)
    return command
  
  def endCommand(self, clientId, commandId):
    command = self._commandDAO.find(commandId)
    if command is None:
      raise NotFoundException()
    if command.clientId != clientId:
      raise NotFoundException()      

    command.endTime = time.time()
    self._commandDAO.save(command)
    return command

  def __init__(self):
    self._commandDAO = None
    self._server = Flask(__name__)

  def setCommandDAO(self, commandDAO):
    self._commandDAO = commandDAO        
    
  def run(self):
    @self._server.route('/client/<clientId>/command', methods=['GET'])
    def getCommand(clientId):
      try:
        command = self.popCommand(clientId)
        return command.json()
      except NotFoundException as e:
        self._shutdownIfNotMoreCommands()      
        msg = "Not found commands for client '%s'" % clientId
        logging.info(msg)
        return msg, 404

    @self._server.route('/client/<clientId>/command/<commandId>', methods=['POST'])
    def postCommand(clientId, commandId):
      try:
        command = self.endCommand(clientId, commandId)
        return command.json()
      except NotFoundException as e:
        return "Command'%s' doesn't exist." % commandId, 500
     
    self._server.run(debug=True, use_reloader=False)
    return []
