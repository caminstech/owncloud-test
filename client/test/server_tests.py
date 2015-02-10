from nose.tools import *
from mockito import *
import unittest

from source.server import *
from source.exception import *
from source.commands.system import *

class MyTestCase(unittest.TestCase):

  def createCommandResponse(self, command): 
    response = mock()
    response.status_code = 200
    when(response).json().thenReturn({ 'command': command })
    return response

  def setResponse(self, response): 
  	when(self.server._requests).get('').thenReturn(response)    

  def setUp(self):
    self.server = Server('')
    self.server._requests = mock()

  def tearDown(self):
    pass

  def test_get(self):
    self.setResponse(self.createCommandResponse('copy'))
    self.assertIsInstance(self.server.get(), Copy)

  def test_get_command_not_found(self):
    self.setResponse(self.createCommandResponse('Not found command'))
    self.assertRaises(CommandNotFoundException, self.server.get)