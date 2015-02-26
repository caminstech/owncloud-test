import shutil
import os.path
import time

from exception import CommandExecutionException

class CopyFile:
  src = None
  dst = None 	
  def set(self, parameters):
    self.src = parameters.get('src')
    self.dst = parameters.get('dst')

    if self.src is None:
      raise CommandParameterNotFoundException('src')

    if self.dst is None:
      raise CommandParameterNotFoundException('dst')

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

    if self.path is None:
      raise CommandParameterNotFoundException('path')

  def run(self):
    while(not self.found()):
      time.sleep(self.wait)

  def __str__(self):
    return "WaitUntilFileSize(path=%s,size=%s)" % (self.path, self.size)

class Wait:
  seconds = None

  def set(self, parameters):
    self.seconds = parameters.get('seconds')

    if self.seconds is None:
      raise CommandParameterNotFoundException('seconds')

  def run(self):
    time.sleep(self.seconds)

  def __str__(self):
    return "Wait(seconds=%s)" % (self.seconds)
