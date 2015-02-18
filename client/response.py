import json
from enum import Enum

class Response:
  class Status(Enum):
    ok = 'ok'
    error = 'error'
    timeout = 'timeout'

  uid = None
  status = None
  message = None

  def json(self):
    return json.dumps({ 'status': self.status.value, 'message': self.message })
