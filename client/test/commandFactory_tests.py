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

  def testCreateMoveFile(self):    
    self.assertIsInstance(self.factory.create(CommandFactory.ID_MOVE_FILE, {'src': 'path1', 'dst': 'path2'}), MoveFile)

  def testCreateCreateFile(self):    
    self.assertIsInstance(self.factory.create(CommandFactory.ID_CREATE_FILE, {'path': 'path1', 'size': '1'}), CreateFile)

  def testCreateWaitFile(self):    
    self.assertIsInstance(self.factory.create(CommandFactory.ID_WAIT_FILE, {'path': 'path1'}), WaitUntilFileSize)

  def testCreateNotFound(self):    
    self.assertRaises(CommandNotFoundException, self.factory.create, ('Not exists'))
