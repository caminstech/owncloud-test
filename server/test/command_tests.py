from mockito import *
import unittest

import json

from command import Command

class CommandTest(unittest.TestCase):
  def createCommandAsDict(self, client = None):
    return { 
      'uid': 'command-uid', 
      'name': 'command-name', 
      'parameters': { 'param1': 'param1-value', 'param2': 'param2-value'}, 
      'startTime': 1, 
      'endTime': 2, 
      'client': client.uid if client is not None else None
    }

  def testJsonWithOutClient(self):
    expected = self.createCommandAsDict()
    command = Command()
    command.uid = expected['uid']
    command.name = expected['name']
    command.parameters = expected['parameters']
    command.startTime = expected['startTime']
    command.endTime = expected['endTime']
    self.assertEquals(expected, json.loads(command.json()))
  
  def testJsonWithClient(self):
    client = mock()
    client.uid = 'client-id'
    expected = self.createCommandAsDict(client)
    command = Command()
    command.uid = expected['uid']
    command.name = expected['name']
    command.parameters = expected['parameters']
    command.startTime = expected['startTime']
    command.endTime = expected['endTime']
    command.client = client
    self.assertEquals(expected, json.loads(command.json()))
