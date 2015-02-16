import shutil

from ..command import Command
from ..server import Response

class Copy(Command): 	
  def run(self):
    shutil.copyfile(self.parameters['src'], self.parameters['dst'])
    response = Response()
    response.uid = Command.uid
    response.status = Response.Status.ok
    response.message = ''
    return response
