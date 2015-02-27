#!/usr/bin/env python3

from command import Command
from client import Client
from server import Server
  
class ServerLoader:
  def load(self, testname):
    # TODO: Load tests dynamically
    clientCopy1 = Client('client-copy-1')
    clientCopy1.addCommand(Command.createWaitFile('file.dat'))
    clientCopy1.addCommand(Command.createCopyFile('file.dat', 'file-1.dat'))
    
    clientCopy2 = Client('client-copy-2')
    clientCopy2.addCommand(Command.createWaitFile('file.dat'))
    clientCopy2.addCommand(Command.createWaitFile('file-1.dat'))
    clientCopy2.addCommand(Command.createCopyFile('file-1.dat', 'file-2.dat'))
    
    clientDownload1 = Client('client-download-1')
    clientDownload1.addCommand(Command.createWaitFile('file.dat'))
    clientDownload1.addCommand(Command.createWaitFile('file-1.dat'))
    clientDownload1.addCommand(Command.createWaitFile('file-2.dat'))
    
    server = Server()
    server.addClient(clientCopy1)
    server.addClient(clientCopy2)
    server.addClient(clientDownload1)
    return server
