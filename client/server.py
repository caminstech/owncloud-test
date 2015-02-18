import urllib3
import requests
from urllib.parse import urljoin

from command import *
from commandFactory import *
from exception import *

class Server:

  baseUrl = None
  clientId = None

  _factory = None
  _requests = None

  def _getClientUrl(self):
    return urljoin(self.baseUrl + '/client/', self.clientId)

  def _createCommand(self, json):
    command = Command()
    command.uid = json['uid']
    command.timeout = json['timeout'] if 'timeout' in json else None
    command.runnable = self._factory.create(json['command'], json['parameters'] if 'parameters' in json else {})
    return command

  def __init__(self, baseUrl, clientId):
    self.baseUrl = baseUrl
    self.clientId = clientId
    self._factory = CommandFactory()
    self._requests = requests

  def get(self):
    url = self._getClientUrl()
    response = self._requests.get(url)
    if response.status_code != requests.codes.ok: 
      raise HttpException(response.status_code)

    return self._createCommand(response.json())
    
  def send(self, response):
    url = self._getClientUrl()
    url = urljoin(url + "/", response.uid)
    self._requests.post(url, response.json())
