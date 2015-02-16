import json
import urllib3
import requests
from enum import Enum
from urllib.parse import urljoin

from client import Client
from command import CommandFactory 
from exception import HttpException

class Response:
  class Status(Enum):
    ok = 'OK'
    error = 'ERROR'
    timeout = 'TIMEOUT'

  uid = None
  status = None
  message = None

  def json(self):
    return json.dumps({ 'uid': self.uid, 'status': self.status, 'message': self.message })

class Server:

  baseUrl = None

  _client = None
  _factory = None
  _requests = None

  def _createCommand(self, json):
    command = self._factory.create(json['command'])
    command.uid = json['uid']
    command.timeout = json['timeout'] if 'timeout' in json else None
    command.parameters = json['parameters'] if 'parameters' in json else {}
    return command

  def __init__(self, baseUrl = ''):
    self.baseUrl = baseUrl
    self._client = Client()
    self._factory = CommandFactory()
    self._requests = requests

  def get(self):
    url = urljoin(self.baseUrl, '/' + self._client.uid)
    response = self._requests.get(url)
    if response.status_code != requests.codes.ok: 
      raise HttpException(response.status_code)

    return self._createCommand(response.json())
    
  def send(self, response):
    url = self.baseUrl
    url = urljoin(url, '/' + self._client.uid)
    url = urljoin(url, '/' + response.uid)
    self._requests.post(url, response.json())