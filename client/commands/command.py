from multiprocessing import Process, Queue
from . import exception

class Command:
  timeout = None
  _output = Queue()

  def my_run(self):
    self._output.put(self.run())

  def run(self):
    raise Exception('No command class defined')

  def execute(self):
    p = Process(target=self.my_run)
    p.start()
    p.join(self.timeout)
    if p.is_alive():
      p.terminate()
      p.join()
      raise exception.TimeOutException()
    if self._output.empty(): 
      return None

    return self._output.get_nowait()

