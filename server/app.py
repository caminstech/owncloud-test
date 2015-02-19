#!/usr/bin/env python3

from flask import Flask

commands = {
  'client1': [
    { 'command': 'copy', 'src': 'a.txt', 'dst': 'b.txt' },
  ],  
  'client2': [
    { 'command': 'wait-file', 'path': 'b.txt' },
  ], 
}

@app.route('/client/<client>/command', methods=['GET'])
def get_command(client):
  return 'Client %s' % client

@app.route('/client/<client>/command/<command>', methods=['POST'])
def post_command(client, command):
  return 'Client %s - %s' % client, command

if __name__ == '__main__':
  app = Flask(__name__)
  app.run()