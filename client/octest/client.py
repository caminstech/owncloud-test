import socket

class Client:
  def __init__(self):
    self.uid = socket.gethostname()
    
  def getUid():
    return self.uid