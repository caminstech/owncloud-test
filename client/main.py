#!/usr/bin/env python3

from sys import argv
from server import Server

class Main:
  def __init__(self, url):
    self.server = Server(url)

  def run(self):
    self.server.connect();
    command = self.server.get()
    while command is not None:
      response = command.execute()
      self.server.send(response)
      command = self.server.get()

main = Main(argv[1]);
main.run()