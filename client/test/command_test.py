from mockito import *
import unittest

from source.command import *
from source.exception import *
from source.commands.system import *
  
class CommandFactoryTestCase(unittest.TestCase):
  def setUp(self):
    self.factory = CommandFactory()

  def testCreateCopy(self):    
    self.assertIsInstance(self.factory.create(CommandFactory.ID_COPY), Copy)

  def testCreateNotFound(self):    
    self.assertRaises(CommandNotFoundException, self.factory.create, (''))