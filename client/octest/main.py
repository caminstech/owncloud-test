#!/usr/bin/env python3

from server import Server
import argparse

class Main:
  def __init__(self, baseurl):
    self.server = Server(baseurl)

  def run(self):
    runner = CommandRunner()
    command = self.server.get()
    while command is not None:
      response = runner.run(command)
      self.server.send(response)
      command = self.server.get()

def parseCommandLine():
	parser = argparse.ArgumentParser()
	parser.add_argument("--baseurl", required=True)
	return parser.parse_args()

args = parseCommandLine()
main = Main(args.baseurl);
main.run()