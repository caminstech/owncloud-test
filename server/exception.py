class NotFoundException(Exception):
  pass

class CommandNotFoundException(Exception):
  pass

class EmptyCommandsException(Exception):
  pass

class WaitingClientsException(Exception):
  pass
