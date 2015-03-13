import shutil
import os.path
import time
import humanfriendly

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
    return "CopyFile(src=%s,dst=%s)" % (self.src, self.dst)

class MoveFile:
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
    if self.src == self.dst: 
      raise CommandExecutionException('src == dst')

    try:
      shutil.move(self.src, self.dst)
    except IOError as e:
      raise CommandExecutionException(e)

  def __str__(self):
    return "MoveFile(src=%s,dst=%s)" % (self.src, self.dst)

class CreateFile:
  path = None
  size = None 	
  
  def _sizeInBytes(self, value):
    if value is None:
      return 0
    return humanfriendly.parse_size(str(value))

  def set(self, parameters):
    self.path = parameters.get('path')
    self.size = self._sizeInBytes(parameters.get('size'))

    if self.path is None:
      raise CommandParameterNotFoundException('path')

  def run(self):
    b = bytearray.fromhex('00')
    try:
      dirname = os.path.dirname(self.path)
      if dirname and not os.path.isdir(dirname):
        os.makedirs(dirname)
      f = open(self.path, 'wb')
      f.seek(self.size-1)
      f.write(b)
      f.close()
    except IOError as e:
      raise CommandExecutionException(e)

  def __str__(self):
    return "CreateFile(path=%s,size=%s)" % (self.path, self.size)

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
