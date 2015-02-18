import time
from multiprocessing import Process, Queue

from response import Response
from exception import *

class CommandRunner:

  def _run(self, runnable, queue):
    try:
      status = 'ok'
      message = runnable.run()
    except CommandExecutionException as e:
      status = 'error'
      message = str(e)
    queue.put({'status': status, 'message': message})

  def _runAsProcess(self, runnable, timeout = None):
    queue = Queue()
    process = Process(target=self._run, args=(runnable,queue))
    process.start()
    process.join(timeout)
    if process.is_alive():
      process.terminate()
      process.join()
      raise CommandTimeOutException()

    if queue.empty():
      raise CommandExecutionException()

    result = queue.get_nowait()
    if result['status'] == 'error':
      raise CommandExecutionException(result['message'])

  def run(self, command):
    response = Response()
    response.status = Response.Status.ok
    try:
      self._runAsProcess(command.runnable, command.timeout)
    except CommandTimeOutException as e:
      response.status = Response.Status.timeout
      response.message = str(e)
    except CommandExecutionException as e:
      response.status = Response.Status.error
      response.message = str(e)

    response.uid = command.uid
    return response