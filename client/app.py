#!/usr/bin/env python3

import argparse

from server import *
from commandRunner import *

class App:
  server = None
  runner = None

  def __init__(self, baseurl, clientid):
    self.server = Server(baseurl, clientid)
    self.runner = CommandRunner()
  
  def run(self):  
    command = self.server.get()
    while command is not None:
      response = self.runner.run(command)
      self.server.send(response)
      command = self.server.get()

def parseCommandLine():
  parser = argparse.ArgumentParser()
  parser.add_argument("--baseurl", required=True)
  parser.add_argument("--clientid", required=True)
  return parser.parse_args()

if __name__ == '__main__':
  args = parseCommandLine()
  app = App(args.baseurl, args.clientid);
  app.run()