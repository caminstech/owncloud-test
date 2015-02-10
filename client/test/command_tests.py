from mockito import *
import unittest

import time

from source.command import *
from source.exception import *
from source.commands.system import *
  
class CommandFactoryTest(unittest.TestCase):
  def setUp(self):
    self.factory = CommandFactory()

  def testCreateCopy(self):    
    self.assertIsInstance(self.factory.create(CommandFactory.ID_COPY), Copy)

  def testCreateNotFound(self):    
    self.assertRaises(CommandNotFoundException, self.factory.create, (''))

class CommandTest(unittest.TestCase):
  class SleepCommand(Command):
    def __init__(self, sleep = None):
      self.sleep = sleep
    
    def run(self):
      if self.sleep is not None:
        time.sleep(self.sleep)

  def testExecute(self):
    command = self.SleepCommand()
    command.execute()

  def testExecuteTimeout(self):
    command = self.SleepCommand(10)
    command.timeout = 0.1;
    self.assertRaises(TimeOutException, command.execute)