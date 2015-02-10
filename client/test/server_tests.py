from mockito import *
import unittest

from source.server import *
from source.exception import *
from source.commands.system import *

class ServerTest(unittest.TestCase):

  def createCommandResponse(self, uid, command, parameters = {}, timeout = None): 
    response = mock()
    response.status_code = 200
    json = { 'command': command, 'parameters': parameters }
    if timeout is not None:
      json['timeout'] = timeout

    when(response).json().thenReturn({ 'uid': uid, 'command': command, 'timeout': timeout, 'parameters': parameters })
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