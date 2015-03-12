from exception import CommandNotFoundException
from commands import system

class CommandFactory:
  ID_WAIT = 'wait'
  ID_CREATE_FILE = 'create-file'
  ID_COPY_FILE = 'copy-file'
  ID_WAIT_FILE = 'wait-file'

  def __init__(self):
    self.commands = { 
      self.ID_WAIT: system.Wait(),
      self.ID_COPY_FILE: system.CopyFile(),
      self.ID_CREATE_FILE: system.CreateFile(),
      self.ID_WAIT_FILE: system.WaitUntilFileSize(),
    }
  
  def create(self, id, parameters = {}):
    if id not in self.commands:
      raise CommandNotFoundException(id)
    command = self.commands.get(id)
    
    command.set(parameters);
    return command
