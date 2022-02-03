#!/usr/bin/env python3

# [!] RUN this only on your supernode

import sys
sys.path.insert(1, 'qpeer')
from node import *
from utils import Utils
import socket
import time
import requests
import _thread

server = Server()
utils = Utils()

def run_server():
	try:
		soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		soc.bind(('', 1691))
		soc.listen(10)
		forward = utils.forward_port()
		if forward:
			while True:
				conn, addr = soc.accept()
				try:
					firstmsg = conn.recv(2048)
					if firstmsg[0] == 'qpeer': #Check msgtype
						_thread.start_new_thread(server.setup, (conn, firstmsg[1],))
					else:
						pass
				except Exception as e:
					print(e)
		else:
			print("Can't map qPeer's port")
			soc.close()

	except Exception as e:
		print(e)
		
	finally:
		utils.close_port()

def internet_check():
	while True:
		try:
			time.sleep(2)
			req = requests.get('https://google.com', timeout=3)
			return True
		except:
			return False

if __name__ == '__main__':
	while internet_check() == True:
		run_server()
	else:
		print("No internet connection")