import shutil
import os.path
import time

from octest.exception import CommandExecutionException

class Copy: 	
  def run(self):
    try:
      shutil.copyfile(self.parameters['src'], self.parameters['dst'])
    except IOError as e:
      raise CommandExecutionException(e)

class WaitUntilFileSize:
  sleep = 1

  def found(self):
      if not os.path.isfile(self.parameters['path']):
        return False

      if self.parameters['size'] is None or self.parameters['size'] == os.path.getsize(self.parameters['path']):
        return True

      return False

  def run(self):
    while(not self.found()):
      time.sleep(self.sleep)

class Wait:
  def run(self):
    time.sleep(self.parameters['wait'])
