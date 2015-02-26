#!/usr/bin/env python3

import json
import uuid
import time

from flask import Flask

class Command:
  uid = None
  name = None
  parameters = None
  startTime = None
  endTime = None
  client = None
  
  def json(self):
    values = {
      'uid': self.uid,
      'command': self.name,
      'parameters': self.parameters,
      'startTime': self.startTime,
      'endTime': self.endTime
    }
    return json.dumps(values)
  
  @staticmethod
  def createWait(seconds):
    c = Command()
    c.uid = str(uuid.uuid4())
    c.name = 'wait'
    c.parameters = { 'seconds': seconds }
    return c

  @staticmethod
  def createWaitFile(path):
    c = Command()
    c.uid = str(uuid.uuid4())
    c.name = 'wait-file'
    c.parameters = { 'path': path }
    return c

  @staticmethod
  def createCopyFile(src, dst):
    c = Command()
    c.uid = str(uuid.uuid4())
    c.name = 'copy-file'
    c.parameters = { 'src': src, 'dst': dst }
    return c
   
class CommandDAO:
  commands = {}
  def add(self, command):
    self.commands.append(command)
    print("-- ADD -----------------------------------------")
    for c in self.commands:
      print(c.json())
    print("------------------------------------------------")
  def update(self, command):
    self.commands.append(command)
    print("-- UPDATE --------------------------------------")
    for c in self.commands:
      print(c.json())
    print("------------------------------------------------")
  def save(self, command):
    self.commands[command.uid] = command
    print("-- SAVE ----------------------------------------")
    for c in self.commands:
      print(c.json())
    print("------------------------------------------------")

class Client:
  uid = None
  commands = None
  
  def __init__(self, uid):
    self.uid = uid
    self.commands = [] 
      
  def add(self, command):
    self.commands.append(command)
    
  def get(self):
    if len(self.commands) == 0:
      return None
    return self.commands.pop(0)

class ClientTester:
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
        
      command = client.get()
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
    
  def run(self):
    self.server.run(debug=True)
    return []

class App: 
  def run(self):
    clientCopy1 = Client('client-copy-1')
    clientCopy1.add(Command.createWaitFile('file.dat'))
    clientCopy1.add(Command.createCopyFile('file.dat', 'file-1.dat'))
    
    clientCopy2 = Client('client-copy-2')
    clientCopy2.add(Command.createWaitFile('file.dat'))
    clientCopy2.add(Command.createWaitFile('file-1.dat'))
    clientCopy2.add(Command.createCopyFile('file-1.dat', 'file-2.dat'))
    
    clientDownload1 = Client('client-download-1')
    clientDownload1.add(Command.createWaitFile('file.dat'))
    clientDownload1.add(Command.createWaitFile('file-1.dat'))
    clientDownload1.add(Command.createWaitFile('file-2.dat'))
    
    clientTester = ClientTester()
    clientTester.addClient(clientCopy1)
    clientTester.addClient(clientCopy2)
    clientTester.addClient(clientDownload1)
    clientTester.run()

app = App()
app.run()
