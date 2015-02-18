import shutil
import os.path
import time

from exception import CommandExecutionException

class Copy:
  src = None
  dst = None 	
  def set(self, parameters):
    self.src = parameters.get('src')
    self.dst = parameters.get('dst')

  def run(self):
    try:
      shutil.copyfile(self.src, self.dst)
    except IOError as e:
      raise CommandExecutionException(e)

  def __str__(self):
    return "Copy(src=%s,dst=%s)" % (self.src, self.dst)


class WaitUntilFileSize:
  path = None
  size = None  
  wait = 1

  def found(self):
      if not os.path.isfile(self.path):
        return False
      if self.size is None or self.size == os.path.getsize(self.path):
        return True
      return False

  def set(self, parameters):
    self.path = parameters.get('path')
    self.size = parameters.get('size')

  def run(self):
    while(not self.found()):
      time.sleep(self.wait)

  def __str__(self):
    return "WaitUntilFileSize(path=%s,size=%s)" % (self.path, self.size)

class Wait:
  wait = None

  def set(self, parameters):
    self.wait = parameters.get('wait')

  def run(self):
    time.sleep(self.wait)

  def __str__(self):
    return "Wait(wait=%s)" % (self.wait)