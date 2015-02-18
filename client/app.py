#!/usr/bin/env python3

import argparse
import logging

from server import *
from commandRunner import *

class App:
  server = None
  runner = None
  logger = None

  def __init__(self, baseurl, clientid):
    self.server = Server(baseurl, clientid)
    self.runner = CommandRunner()
    self.logger = logging.getLogger(__name__)
  
  def run(self):  
    self.logger.info("Client started.")
    command = self.server.get()
    while command is not None:
      self.logger.info("Command read %s." % str(command))

      response = self.runner.run(command)
      self.server.send(response)
      command = self.server.get()

def parseCommandLine():
  parser = argparse.ArgumentParser()
  parser.add_argument("--baseurl", required=True)
  parser.add_argument("--clientid", required=True)
  parser.add_argument("--loglevel", default="INFO")
  parser.add_argument("--logfile", default="app.log")
  return parser.parse_args()

def configLogging(args):
  level = getattr(logging, args.loglevel.upper(), None)
  if not isinstance(level, int):
    raise ValueError('Invalid log level: %s' % args.loglevel)
  format = '%(asctime)-15s %(message)s'
  logging.basicConfig(format=format, filename=args.logfile, level=level)

if __name__ == '__main__':
  args = parseCommandLine()
  configLogging(args)
  app = App(args.baseurl, args.clientid);
  app.run()