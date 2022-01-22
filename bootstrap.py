#!/usr/bin/env python3

# [!] RUN this only on your supernode

import sys
sys.path.insert(1, 'qpeer')
from node import *
import socket
import _thread

server = Server()

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind(('', 1691))
soc.listen(10)

def run_server():
	while True:
		conn, addr = soc.accept()
		try:
			_thread.start_new_thread(server.setup, (conn, ))
		except Exception as e:
			print(e)

if __name__ == '__main__':
	print("Srv running")
	run_server()	