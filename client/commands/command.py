from multiprocessing import Process, Queue
from exception import TimeOutException

class Command:
  timeout = None
  _output = Queue()

  def my_run(self):
    self._output.put(self.run())

  def execute(self):
    p = Process(target=self.my_run)
    p.start()
    p.join(self.timeout)
    if p.is_alive():
      p.terminate()
      p.join()
      raise TimeOutException()
    if self._output.empty(): 
      return None

    return self._output.get_nowait()

