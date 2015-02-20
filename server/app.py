#!/usr/bin/env python3

import json
import uuid
import time

from flask import Flask

def commandWaitFile(path):
  return {
    'uid': str(uuid.uuid4()),
    'command': 'wait-file',
    'parameters': {
      'path': path
    }
  }

def commandCopyFile(src, dst):
  return {
    'uid': str(uuid.uuid4()),
    'command': 'copy-file',
    'parameters': {
      'src': src,
      'dst': dst
    }
  }

executed = {
}

pending = {
  'client-upload': [],
  'client-download1': [],
  'client-download2': [],
}

pending['client-upload'].append(commandCopyFile('file-0.dat', 'file.dat'));
pending['client-download1'].append(commandWaitFile('file.dat'));
pending['client-download2'].append(commandWaitFile('file.dat'));

app = Flask(__name__)

@app.route('/client/<client>/command', methods=['GET'])
def get_command(client):
  if len(pending[client]) == 0:
    return 'Empty pending.', 404

  command = pending[client].pop(0)
  executed[command.get('uid')] = {
    'ts-get': time.time() 
  }
  return json.dumps(command)

@app.route('/client/<client>/command/<command>', methods=['POST'])
def post_command(client, command):
  executed[command]['time-post'] = time.time()
  return json.dumps(executed[command])

if __name__ == '__main__':
  app.run(debug=True)
  app.run()