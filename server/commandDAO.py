import logging
import json

from collections import OrderedDict

from command import Command

class CommandDAO:
  _database = None

  def _createFromRow(self, row):
    if row is None: 
      return None
    command = Command()
    (command.uid, command.name, parameters, command.startTime, command.endTime, command.clientId, command.order) = row
    command.parameters = json.loads(parameters)
    return command

  def __init__(self, database):
    self._database = database

  def create(self):
    logging.debug("CommandDAO.create()")
    self._database.execute('create table commands (uid text, name text, parameters text, start_time integer, end_time integer, client_id text, c_order integer)')

  def find(self, uid):    
    found = self._database.findByPk('commands', 'uid', uid)
    return self._createFromRow(found)
  
  def findNextFromClient(self, clientId):
    found = self._database.findByCondition('commands', 'start_time is null and client_id=:client_id', {'client_id': clientId}, orderBy='c_order asc')
    return self._createFromRow(found)

  def countPendings(self, clientId = None):
    if clientId is None:
      count = self._database.countByCondition('commands', 'end_time is null')
    else:
      count = self._database.countByCondition('commands', 'end_time is null and client_id=:client_id', {'client_id': clientId})
    return count

  def save(self, command):
    found = self._database.findByPk('commands', 'uid', command.uid)
    values = {}
    values['uid'] = command.uid
    values['name'] = command.name
    values['parameters'] = json.dumps(command.parameters)
    values['start_time'] = command.startTime
    values['end_time'] = command.endTime
    values['client_id'] = command.clientId
    values['c_order'] = command.order
    if found is None:
      self._database.insert('commands', values)
    else :
      self._database.update('commands', 'uid', values)
