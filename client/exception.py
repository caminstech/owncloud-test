class HttpException(Exception):
  pass

class CommandTimeOutException(Exception):
  pass

class CommandExecutionException(Exception):
  pass  

class CommandNotFoundException(Exception):
  pass

class CommandParameterNotFoundException(Exception):
  pass

class CommandWithoutResultException(Exception):
  pass