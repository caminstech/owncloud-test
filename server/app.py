#!/usr/bin/env python3
import argparse
import logging

from database import DatabaseSQLite
from command import Command
from commandDAO import CommandDAO
from server import Server
from testLoader import TestLoader
  
class App:
  def __init__(self, testname, database, newDatabase = False):    
    commandDAO = CommandDAO(DatabaseSQLite(database))
    if newDatabase:
      logging.debug("App() - Creating CommandDAO tables.")
      commandDAO.create()

    testLoader = TestLoader()
    testLoader.setCommandDAO(commandDAO)
    testLoader.load(testname)

    self.server = Server()
    self.server.setCommandDAO(commandDAO)
  
  def run(self):    
    self.server.run()

def parseCommandLine():
  parser = argparse.ArgumentParser()
  parser.add_argument('--testname', required=True)
  parser.add_argument('--database', required=True)
  parser.add_argument('--new-database', action='store_true')
  parser.add_argument('--loglevel', default='INFO')
  parser.add_argument('--logfile', default=__name__ + '.log')
  return parser.parse_args()

def configLogging(args):
  level = getattr(logging, args.loglevel.upper(), None)
  if not isinstance(level, int):
    raise ValueError('Invalid log level: %s' % args.loglevel)
  format = '%(asctime)s - %(filename)s#%(lineno)s - %(message)s'
  logging.basicConfig(format=format, filename=args.logfile, level=level)

if __name__ == '__main__':
  args = parseCommandLine()
  configLogging(args)  
  app = App(args.testname, args.database, args.new_database)
  app.run()
