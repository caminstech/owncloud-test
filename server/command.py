import json
import uuid

class Command:
  uid = None
  name = None
  parameters = None
  startTime = None
  endTime = None
  client = None
  
  def json(self):
    values = {
      'uid': self.uid,
      'command': self.name,
      'parameters': self.parameters,
      'startTime': self.startTime,
      'endTime': self.endTime,
      'client': self.client.uid if self.client is not None else None
    }
    return json.dumps(values)
  
  @staticmethod
  def createWait(seconds):
    c = Command()
    c.uid = str(uuid.uuid4())
    c.name = 'wait'
    c.parameters = { 'seconds': seconds }
    return c

  @staticmethod
  def createWaitFile(path):
    c = Command()
    c.uid = str(uuid.uuid4())
    c.name = 'wait-file'
    c.parameters = { 'path': path }
    return c

  @staticmethod
  def createCopyFile(src, dst):
    c = Command()
    c.uid = str(uuid.uuid4())
    c.name = 'copy-file'
    c.parameters = { 'src': src, 'dst': dst }
    return c

class CommandDAO:
  database = None

  def __init__(self, database):
    self.database = database

  def add(self, command):
    pass

  def update(self, command):
    pass

  def save(self, command):
    pass
