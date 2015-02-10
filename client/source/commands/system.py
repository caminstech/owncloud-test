import shutil

from ..command import Command

class Copy(Command): 	
  def run(self):
    shutil.copyfile(self.parameters['src'], self.parameters['dst'])
