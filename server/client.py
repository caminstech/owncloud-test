class Client:
  _uid = None
  _commands = None
  
  def __init__(self, uid):
    self._uid = uid
    self._commands = [] 
      
  def getUid(self):
    return self._uid;

  def getCommands(self):
    return self._commands

  def addCommand(self, command):
    self._commands.append(command)
    
  def popCommand(self):
    if len(self._commands) == 0:
      return None
    return self._commands.pop(0)
