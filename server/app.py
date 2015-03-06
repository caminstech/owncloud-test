#!/usr/bin/env python3
import argparse
import logging

from exception import NotFoundException, ValueErrorException
from database import DatabaseSQLite
from command import Command
from commandDAO import CommandDAO
from server import Server
from testLoader import TestLoader
  
class App:
  def __init__(self, database, newDatabase = False):    
    commandDAO = CommandDAO(DatabaseSQLite(database))
    if newDatabase:
      logging.debug("App() - Creating CommandDAO tables.")
      commandDAO.create()

    self.testLoader = TestLoader()
    self.testLoader.setCommandDAO(commandDAO)

    self.server = Server()
    self.server.setCommandDAO(commandDAO)
  
  def run(self, testname):    
    try:
      self.testLoader.load(testname)
      self.server.run()
    except NotFoundException as e:
      print('ERROR: ' + str(e))
    except ValueErrorException as e:
      print('ERROR: ' + str(e))

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
  app = App(args.database, args.new_database)
  app.run(args.testname)
