import json
import urllib3
import requests

from command import CommandFactory 
from exception import HttpException

class Server:
  _url = None
  _factory = None
  _requests = None

  def _parse(self, json):
    values = {}
    values['uid'] = json['uid']
    values['command'] = json['command']
    values['timeout'] = json['timeout'] if 'timeout' in json else None
    values['parameters'] = json['parameters'] if 'parameters' in json else {}
    return values

  def __init__(self, url = ''):
    self._url = url
    self._factory = CommandFactory()
    self._requests = requests

  def get(self):
    response = self._requests.get(self._url)
    if response.status_code != requests.codes.ok: 
      raise HttpException(response.status_code)

    values = self._parse(response.json())
    command = self._factory.create(values['command'])
    command.uid = values['uid']
    command.timeout = values['timeout']
    command.parameters = values['parameters']
    return command
  
  def send(self, response):
    self._requests
    print(response)