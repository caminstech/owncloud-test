import uuid
import json

from command import Command
from exception import ValueErrorException, NotFoundException

class TestLoader:
  _commandDAO = None

  def _createCommand(self, name, parameters):
    command = Command()
    command.name = name
    command.parameters = parameters
    return command

  def _addClientToDAO(self, clientId, commands):
    order = 1
    for command in commands:
      command.uid = str(uuid.uuid4())
      command.clientId = clientId
      command.order = order
      self._commandDAO.save(command)
      order += 1
  
  def _loadTest(self, test):
    profiles = self._loadProfiles(test)
    clients = self._loadClients(test)
    for (client,profile) in clients.items():
      self._addClientToDAO(client, profiles[profile])

  def _loadProfiles(self, test):
    profiles = {}
    for (name,commands) in test['profiles'].items():
      profiles[name] = []
      for command in commands:      
        profiles[name].append(self._createCommand(command['name'], command['parameters']))
    return profiles
     
  def _loadClients(self, test):
    return test['clients']

  def setCommandDAO(self, commandDAO):
    self._commandDAO = commandDAO        

  def load(self, testname):
    try:
      jsonFile = open(testname)
      test = json.load(jsonFile)
      jsonFile.close()
    except IOError as e:
      raise NotFoundException('File %s not found' % testname)
    except ValueError as e:
      raise ValueErrorException('File %s is not a valid JSON file' % testname)

    self._loadTest(test)
