from mockito import *
import unittest

import json

from command import Command

class CommandTest(unittest.TestCase):
  def createCommandAsDict(self, clientId, order):
    return { 
      'uid': 'command-uid', 
      'name': 'command-name', 
      'parameters': { 'param1': 'param1-value', 'param2': 'param2-value'}, 
      'startTime': 1, 
      'endTime': 2, 
      'clientId': clientId,
      'order': order
    }

  def testJsonWithOutClient(self):
    expected = self.createCommandAsDict(None, None)
    command = Command()
    command.uid = expected['uid']
    command.name = expected['name']
    command.parameters = expected['parameters']
    command.startTime = expected['startTime']
    command.endTime = expected['endTime']
    command.clientId = expected['clientId']
    command.order = expected['order']
    self.assertEquals(expected, json.loads(command.json()))
  
  def testJsonWithClient(self):
    expected = self.createCommandAsDict('client1', 1)
    command = Command()
    command.uid = expected['uid']
    command.name = expected['name']
    command.parameters = expected['parameters']
    command.startTime = expected['startTime']
    command.endTime = expected['endTime']
    command.clientId = expected['clientId']
    command.order = expected['order']
    self.assertEquals(expected, json.loads(command.json()))
