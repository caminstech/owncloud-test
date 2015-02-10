from command import Command

import shutil

class Copy(Command): 	
  def run(self):
    shutil.copyfile(self.parameters['src'], self.parameters['dst'])
