from octest.exception import CommandNotFoundException
from octest.commands import system

class CommandFactory:
  ID_COPY = 'copy'
  ID_WAIT = 'wait'
  ID_WAIT_FILE = 'wait-file'

  def __init__(self):
    self.commands = { 
      self.ID_COPY: system.Copy(),
      self.ID_WAIT: system.Wait(),
      self.ID_WAIT_FILE: system.WaitUntilFileSize(),
    }
  
  def create(self, commandId):
    if commandId not in self.commands:
      raise CommandNotFoundException(commandId)
    return self.commands[commandId]