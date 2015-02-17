import shutil

from octest.exception import CommandExecutionException

class Copy: 	
  def run(self):
    try:
      shutil.copyfile(self.parameters['src'], self.parameters['dst'])
    except IOError as e:
      raise CommandExecutionException(e)