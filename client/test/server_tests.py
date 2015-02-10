from mockito import *
import unittest
import json

from source.server import *
from source.exception import *
from source.command import * 
from source.commands.system import *

class ServerTest(unittest.TestCase):

  def createCommandResponse(self, uid, command, parameters = {}, timeout = None): 
    response = mock()
    response.status_code = 200
    json = { 'uid': uid, 'command': command, 'parameters': parameters }
    if timeout is not None:
      json['timeout'] = timeout

    when(response).json().thenReturn(json)
    return response

  def setResponse(self, response): 
  	when(self.server._requests).get('').thenReturn(response)    

  def setUp(self):
    self.server = Server('')
    self.server._requests = mock()

  def testGet(self):
    self.setResponse(self.createCommandResponse(uid = 'a00001', command = 'copy', parameters = {'src': 'source', 'dst': 'destination' }, timeout = 10))
    response = self.server.get()
    self.assertIsInstance(response, Copy)
    self.assertEqual(response.uid, 'a00001')
    self.assertEqual(response.parameters, {'src': 'source', 'dst': 'destination', })
    self.assertIs(response.timeout, 10)

  def testGetCommandNotFound(self):
    self.setResponse(self.createCommandResponse(uid = 'a00002', command = 'Not found command'))
    self.assertRaises(CommandNotFoundException, self.server.get)

  def testSend(self):
    response = {}
    response['uid'] = 'a00001'
    response['status'] = 'OK'
    self.server.send(response)
    verify(self.server._requests).post('/' + response['uid'], json.dumps(response))
