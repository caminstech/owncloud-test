from mockito import *
import unittest
import time

from command import *
from commandRunner import *
from exception import *
  
class CommandRunnerTest(unittest.TestCase):
  def setUp(self):
    self.runner = CommandRunner()
    self.command = Command()

  def testRun(self):    
    class Runnable:
      def run(self):
        pass
  
    self.command.runnable = Runnable()
    self.command.timeout = None
    response = self.runner.run(self.command)
    self.assertEqual(Response.Status.ok.value, response.status.value)

  def testRunError(self):   
    class RunnableError:
      def run(self):
        raise CommandExecutionException()
 
    self.command.runnable = RunnableError()
    response = self.runner.run(self.command)
    self.assertEqual(Response.Status.error.value, response.status.value)
  
  def testExecuteTimeout(self):
    class RunnableSleep:
      def run(self):
        time.sleep(10)

    self.command.timeout = 0.1
    self.command.runnable = RunnableSleep()
    response = self.runner.run(self.command)
    self.assertEqual(Response.Status.timeout.value, response.status.value)