from octest.exception import CommandNotFoundException
from octest.commands import system

class CommandFactory:
  ID_COPY = 'copy'

  def __init__(self):
    self.commands = { 
      self.ID_COPY: system.Copy() 
    }
  
  def create(self, commandId):
    if commandId not in self.commands:
      raise CommandNotFoundException(commandId)
    return self.commands[commandId]