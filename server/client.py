class Client:
  uid = None
  commands = None
  
  def __init__(self, uid):
    self.uid = uid
    self.commands = [] 
      
  def addCommand(self, command):
    self.commands.append(command)
    
  def getCommand(self):
    if len(self.commands) == 0:
      return None
    return self.commands.pop(0)
