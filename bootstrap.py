#!/usr/bin/env python3

# [!] RUN this only on your supernode

import sys
sys.path.insert(1, 'qpeer')
from node import Server, Client
from errors import *
from utils import Utils
utils = Utils()
import socket
import time
import requests
import json
import threading

server = Server()
print(utils.peerip)

def run_server():
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.bind(('', 1691))
	soc.listen(10)
	try:
		forward = utils.forward_port()
		if forward:
			while True:
				conn, addr = soc.accept()
				try:
					firstmsg = json.loads(conn.recv(2048).decode())
					if firstmsg[0] == 'qpeer': #Check msgtype
						threading.Thread(target=server.setup, args=(conn, firstmsg[1],)).start()
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