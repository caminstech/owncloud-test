import socket

class Client:
  uid = None
  def __init__(self):
    self.uid = socket.gethostbyname(socket.gethostname())