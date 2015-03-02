from mockito import *
import unittest

from client import Client

class ClientTest(unittest.TestCase):
  client = None

  def setUp(self):
    self.client = Client('client-id')

  def testGetNoCommand(self):
    self.assertIsNone(self.client.popCommand())

  def testGetAllCommands(self):
    command1 = mock()
    command2 = mock()
    self.client.addCommand(command1)
    self.client.addCommand(command2)

    self.assertEquals(command1, self.client.popCommand())
    self.assertEquals(command2, self.client.popCommand())
    self.assertIsNone(self.client.popCommand())
