from mockito import *
import unittest
import json

from source.server import *
from source.exception import *
from source.command import * 
from source.commands.system import *

class ServerTest(unittest.TestCase):

  def _createCommandResponse(self, uid, command, parameters = {}, timeout = None): 
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

  def testGetCommmandCopy(self):
    uid = 'XXXXXX'
    command = 'copy'
    parameters = {'src': 'source', 'dst': 'destination' }
    timeout = 10
    self.setResponse(self._createCommandResponse(uid, command, parameters, timeout))

    response = self.server.get()
    
    self.assertIsInstance(response, Copy)
    self.assertEqual(response.uid, uid)
    self.assertEqual(response.parameters, parameters)
    self.assertIs(response.timeout, timeout)

  def testGetCommandNotFound(self):
    uid = 'XXXXXX'
    command = 'Not found command'

    self.setResponse(self._createCommandResponse(uid, command))
    self.assertRaises(CommandNotFoundException, self.server.get)

  def testSendResponseAsJson(self):
    response = {}
    response['uid'] = 'XXXXXX'
    response['status'] = Server.Status.ok
    self.server.send(response)
    verify(self.server._requests).post('/' + response['uid'], json.dumps(response))
