import json
import urllib3
import requests

from command import CommandFactory 
from exception import HttpException

class Server:
  url = None
  factory = None

  def __init__(self, url = ''):
    self.url = url
    self.factory = CommandFactory()

  def get(self):
    response = requests.get(self.url)
    if response.status_code != requests.codes.ok: 
      raise HttpException(response.status_code)

    json = response.json();
    command = self.factory.create(json['command'])
    command.parameters = json['parameters'] if 'parameters' in json else None
    command.timeout = json['timeout'] if 'timeout' in json else None
    return command
  
  def send(self, response):
     print(response)