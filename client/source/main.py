#!/usr/bin/env python3

from server import Server
import argparse

class Main:
  def __init__(self, url):
    self.server = Server(url)

  def run(self):
    command = self.server.get()
    while command is not None:
      response = command.execute()
      self.server.send(response)
      command = self.server.get()

def parseCommandLine():
	parser = argparse.ArgumentParser()
	parser.add_argument("--url", required=True)
	return parser.parse_args()

args = parseCommandLine()
main = Main(args.url);
main.run()