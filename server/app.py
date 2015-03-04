#!/usr/bin/env python3
import argparse
import logging

from command import Command
from database import DatabaseSQLite
from client import Client
from server import Server
from serverLoader import ServerLoader
  
class App:
  server = None
  def __init__(self, testname, database):
    self.server = ServerLoader().load(testname, database)
    
  def run(self):
    self.server.run()

def parseCommandLine():
  parser = argparse.ArgumentParser()
  parser.add_argument('--testname', required=True)
  parser.add_argument('--database', required=True)
  parser.add_argument('--loglevel', default='INFO')
  parser.add_argument('--logfile', default=__name__ + '.log')
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
  app = App(args.testname, args.database)
  app.run()
