import json
import urllib3
import requests

from command import CommandFactory 

class Http:
  def getJson(self):
    return [ 
      { 'command': 'copy', 'timeout': 1, 'parameters': { 'src': 'file1.txt', 'dst' : 'file1-new.txt' } },
      { 'command': 'copy', 'timeout': 1, 'parameters': { 'src': 'folder'   , 'dst' : 'folder-new' } },
    ]

class Response:
  def __init__(self):
    self.status = None
    self.data = None

class Server:
  _url = None
  _http = None
  _factory = None
  _commands = None
  _index = None

  def __init__(self, url = ''):
    self._url = url
    self._factory = CommandFactory()
    self._http = Http()
    self.http = urllib3.PoolManager()

  def connect(self):
    self._commands = self._http.getJson();
    self._index = 0
  
  def get(self):
    response = requests.get(self._url)
    if response.status_code != requests.codes.ok: 
      raise HttpException("Server connection error code {}.".format(response.status_code))

    print(response.json());

    if self._index >= len(self._commands):
      return None

    current = self._commands[self._index]
    self._index += 1

    return self._factory.create(current['command']); 
  
  def send(self, response):
     print(response)