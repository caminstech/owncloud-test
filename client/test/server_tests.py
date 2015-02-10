from nose.tools import *
from mockito import *
import unittest

from source.server import *
from source.exception import *
from source.commands.system import *

class MyTestCase(unittest.TestCase):

  def createCommandResponse(self, command, parameters = {}, timeout = None): 
    response = mock()
    response.status_code = 200
    json = { 'command': command, 'parameters': parameters }
    if timeout is not None:
      json['timeout'] = timeout

    when(response).json().thenReturn({ 'command': command, 'timeout': timeout, 'parameters': parameters })
    return response

  def setResponse(self, response): 
  	when(self.server._requests).get('').thenReturn(response)    

  def setUp(self):
    self.server = Server('')
    self.server._requests = mock()

  def tearDown(self):
    pass

  def test_get(self):
    self.setResponse(self.createCommandResponse('copy', parameters = {'src': 'source', 'dst': 'destination' }, timeout = 10))
    response = self.server.get()
    self.assertIsInstance(response, Copy)
    self.assertEqual(response.parameters, {'src': 'source', 'dst': 'destination', })
    self.assertIs(response.timeout, 10)

  def test_get_command_not_found(self):
    self.setResponse(self.createCommandResponse('Not found command'))
    self.assertRaises(CommandNotFoundException, self.server.get)