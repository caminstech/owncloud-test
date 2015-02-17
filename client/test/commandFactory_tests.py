from mockito import *
import unittest
import time

from octest.commandFactory import *
from octest.commands.system import *
from octest.exception import *
  
class CommandFactoryTest(unittest.TestCase):
  def setUp(self):
    self.factory = CommandFactory()

  def testCreateCopy(self):    
    self.assertIsInstance(self.factory.create(CommandFactory.ID_COPY), Copy)

  def testCreateNotFound(self):    
    self.assertRaises(CommandNotFoundException, self.factory.create, (''))