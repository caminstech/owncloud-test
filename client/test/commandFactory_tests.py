from mockito import *
import unittest
import time

from commandFactory import *
from commands.system import *
from exception import *
  
class CommandFactoryTest(unittest.TestCase):
  def setUp(self):
    self.factory = CommandFactory()

  def testCreateWait(self):    
    self.assertIsInstance(self.factory.create(CommandFactory.ID_WAIT, {'seconds': 1}), Wait)

  def testCreateCopyFile(self):    
    self.assertIsInstance(self.factory.create(CommandFactory.ID_COPY_FILE, {'src': 'path1', 'dst': 'path2'}), CopyFile)

  def testCreateWaitFile(self):    
    self.assertIsInstance(self.factory.create(CommandFactory.ID_WAIT_FILE, {'path': 'path1'}), WaitUntilFileSize)

  def testCreateNotFound(self):    
    self.assertRaises(CommandNotFoundException, self.factory.create, ('Not exists'))
