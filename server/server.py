import json
import time

import logging

from flask import Flask, request

from command import Command, CommandDAO
from exception import ClientNotFoundException, CommandNotFoundException, EmptyCommandsException, WaitingClientsException

class Server:
  clients = None
  clientsWaiting = None
  commands = None
  _commandDAO = None
  _server = None

  def clientMustWait(self, client):
    self.clientsWaiting[client.getUid()] = client    
    return len(self.clients) > len(self.clientsWaiting)

  def createWaitCommand(self):
    seconds = len(self.clients) - len(self.clientsWaiting)
    return Command.createWait(seconds)

  def popCommand(self, clientId):
    client = self.clients.get(clientId)
    if client is None:
      raise ClientNotFoundException()      
    if self.clientMustWait(client):
      raise WaitingClientsException()
    command = client.popCommand()
    if command is None: 
      raise EmptyCommandsException()
    return command
  
  def getCommand(self, clientId, commandId):
    client = self.clients.get(clientId)
    if client is None:
      raise ClientNotFoundException()      
    command = self.commands.get(commandId)
    if command is None:
      raise CommandNotFoundException()      
    if command.client.getUid() != clientId:
      raise CommandNotFoundException()      

    return command

  def shutdown(self):
    logging.info("Server.shutdown(): Shutdown server")
    function = request.environ.get('werkzeug.server.shutdown')
    if function is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    function()

  def __init__(self):
    self.clients = {}
    self.clientsWaiting = {}
    self.commands = {}
    self._commandDAO = None
    self._server = Flask(__name__)

  def setCommandDAO(self, commandDAO):
    self._commandDAO = commandDAO        
       
  def addClient(self, client):
    self.clients[client.getUid()] = client
    for command in client.getCommands():
      self.commands[command.uid] = command
    
  def run(self):
    @self._server.route('/client/<clientId>/command', methods=['GET'])
    def getCommand(clientId):
      try:
        command = self.popCommand(clientId)
        command.startTime = time.time()
        self._commandDAO.save(command)
        return command.json()
      except ClientNotFoundException as e:
        msg = "Client doesn't exist. (clientId=%s)" % clientId
        logging.warning(msg)
        return msg, 500
      except EmptyCommandsException as e:
        self.clients.pop(clientId)
        if len(self.clients) == 0:
          self.shutdown()
        msg = "Empty commands queue. (clientId=%s)" % clientId
        logging.info(msg)
        return msg, 404
      except WaitingClientsException as e:
        msg = "Client must wait. (clientId=%s)" % clientId
        logging.info(msg)
        return self.createWaitCommand().json()

    @self._server.route('/client/<clientId>/command/<commandId>', methods=['POST'])
    def postCommand(clientId, commandId):
      try:
        command = self.getCommand(clientId, commandId)
        command.endTime = time.time()
        self._commandDAO.save(command)
        return command.json()
      except ClientNotFoundException as e:
        return "Client '%s' doesn't exist." % clientId, 500
      except CommandNotFoundException as e:
        return "Command'%s' doesn't exist." % commandId, 500
     
    self._server.run(debug=True, use_reloader=False)
    return []
