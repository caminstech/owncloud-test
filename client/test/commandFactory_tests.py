from mockito import *
import unittest
import time

from commandFactory import *
from commands.system import *
from exception import *
  
class CommandFactoryTest(unittest.TestCase):
  def setUp(self):
    self.factory = CommandFactory()

  def testCreateCopy(self):    
    self.assertIsInstance(self.factory.create(CommandFactory.ID_COPY), Copy)

  def testCreateWait(self):    
    self.assertIsInstance(self.factory.create(CommandFactory.ID_WAIT), Wait)

  def testCreateWaitFile(self):    
    self.assertIsInstance(self.factory.create(CommandFactory.ID_WAIT_FILE), WaitUntilFileSize)

  def testCreateNotFound(self):    
    self.assertRaises(CommandNotFoundException, self.factory.create, ('Not exists'))