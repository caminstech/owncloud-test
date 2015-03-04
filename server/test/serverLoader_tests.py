from mockito import *
import unittest

from server import Server
from serverLoader import ServerLoader

class ServerLoaderTest(unittest.TestCase):
  def testLoad(self):
    server = ServerLoader().load(mock(), mock())
    self.assertIsInstance(server, Server)
