import json
import urllib3
import requests

from command import CommandFactory 
from exception import HttpException

class Server:
  _url = None
  _factory = None
  _requests = None

  def __init__(self, url = ''):
    self._url = url
    self._factory = CommandFactory()
    self._requests = requests

  def get(self):
    response = self._requests.get(self._url)
    if response.status_code != requests.codes.ok: 
      raise HttpException(response.status_code)

    json = response.json();
    command = self._factory.create(json['command'])
    command.parameters = json['parameters'] if 'parameters' in json else None
    command.timeout = json['timeout'] if 'timeout' in json else None
    return command
  
  def send(self, response):
     print(response)