import json
import time

from flask import Flask

from command import Command, CommandDAO

class Server:
  server = None
  clients = None
  clientsWaiting = None
  commands = None
  commandDAO = None
  
  def mustWait(self, client):
    self.clientsWaiting[client.uid] = client    
    if len(self.clients) == len(self.clientsWaiting):
      return 0      
    return 1
  
  def __init__(self):
    self.clients = {}
    self.clientsWaiting = {}
    self.commands = {}
    self.commandDAO = CommandDAO()    
    self.server = Flask(__name__)
    
    @self.server.route('/client/<clientId>/command', methods=['GET'])
    def getCommand(clientId):
      client = self.clients.get(clientId)
      if client is None:
        return "Client doesn't exists.", 500
      
      seconds = self.mustWait(client)
      if seconds != 0:
        return Command.createWait(seconds).json()
        
      command = client.popCommand()
      if command is None: 
        return 'Empty pending.', 404
        
      command.startTime = time.time()
      self.commandDAO.save(command)
      return command.json()
      
    @self.server.route('/client/<clientId>/command/<commandId>', methods=['POST'])
    def postCommand(clientId, commandId):
      client = self.clients.get(clientId)
      if client is None:
        return "Client doesn't exists.", 500

      command = self.commands.get(commandId)
      if command is None:
        return "Command doesn't exists.", 500
      
      command.endTime = time.time()
      self.commandDAO.save(command)
      return json.dumps([])
      
  def addClient(self, client):
    self.clients[client.uid] = client
    for command in client.commands:
      self.commands[command.uid] = command
    
  def run(self, database):
    self.commandDAO = CommandDAO(database)
    self.server.run(debug=True)
    return []
