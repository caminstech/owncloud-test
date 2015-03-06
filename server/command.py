import json

from collections import OrderedDict

class Command:
  uid = None
  name = None
  parameters = None
  startTime = None
  endTime = None
  clientId = None
  order = None
    
  def values(self):
    return OrderedDict({
      'uid': self.uid,
      'name': self.name,
      'parameters': self.parameters,
      'startTime': self.startTime,
      'endTime': self.endTime,
      'clientId': self.clientId,
      'order': self.order,
    })
  
  def json(self):
    return json.dumps(self.values())
