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

  def _getClientCommandUrl(self):
    url = self.baseUrl
    url = urljoin(url, 'client')
    url = urljoin(url + "/", self.clientId)
    url = urljoin(url + "/", 'command')
    return url

  def _createCommand(self, json):
    command = Command()
    command.uid = json.get('uid')
    command.timeout = json.get('timeout')
    command.runnable = self._factory.create(json.get('command'), json.get('parameters'))
    return command

  def __init__(self, baseUrl, clientId):
    self.baseUrl = baseUrl
    self.clientId = clientId
    self._factory = CommandFactory()
    self._requests = requests

  def get(self):
    url = self._getClientCommandUrl()
    response = self._requests.get(url)
    
    if response.status_code == requests.codes.not_found: 
      return None
    
    if response.status_code != requests.codes.ok: 
      raise HttpException(response.status_code)

    return self._createCommand(response.json())
    
  def send(self, response):
    url = self._getClientCommandUrl()
    url = urljoin(url + "/", response.uid)
    self._requests.post(url, response.json())
