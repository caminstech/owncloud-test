from multiprocessing import Process, Queue
from exception import TimeOutException, CommandNotFoundException

class CommandFactory:
  ID_COPY = 'copy'

  def __init__(self):
    from commands import system
    self.commands = { 
      self.ID_COPY: system.Copy() 
    }
  
  def create(self, commandId):
    if commandId not in self.commands:
      raise CommandNotFoundException(commandId)
    return self.commands[commandId]


class Command:
  parameters = {}
  timeout = None
  
  _output = Queue()

  def _my_run(self):
    self._output.put(self.run())

  def execute(self):
    p = Process(target=self._my_run)
    p.start()
    p.join(self.timeout)
    if p.is_alive():
      p.terminate()
      p.join()
      raise TimeOutException()
    if self._output.empty(): 
      return None

    return self._output.get_nowait()