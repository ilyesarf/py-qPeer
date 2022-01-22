#!/usr/bin/env python3

import sys
sys.path.insert(1, 'qpeer')
from node import *
from errors import *
from utils import *
utils = Utils()
from multiprocessing import Process
import socket
import _thread
import random

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
			pass


client = Client()

def run_client():
	if len(client.peers) > 0:
		if len(client.temp_peers) > 0:
			peer = random.choice(client.temp_peers)
			try:
				client.setup(peer[1], peer[2])
				client.temp_peers.remove(peer)
			except socket.error:
				client.temp_peers.remove(peer)
				client.offline_peers.append(peer)
			except Exception as e:
				print(e)
		else:
			peer = utils.decrypt_peer(random.choice(client.peers))
			peerinfo = peer[1]
			try:
				client.setup(peerinfo[1], peerinfo[2])
			except socket.error:
				utils.remove_peer(peer[0])
			except Exception as e:
				print(e)
				
	else: #Bootstrap
		ip = '' #Set the supernode ip (hard-coded node)
		port = 1691
		try:
			client.setup(ip, port)
		except Exception as e:
			print(e)

def ping_client():
	if len(client.peers) > 5:
		peer = random.choice(client.peers)		
		client.ping(peer[0])
	else:
		pass

def internet_check():
	try:
		soc.connect(('1.1.1.1', 80))
		return True
	except socket.error:
		print("No internet connection!")
		return False
		sys.exit()

def main():
	p1 = Process(target=run_server)
	p1.start()

	p2 = Process(target=run_client)
	p2.start()

	p3 = Process(target=ping_client)
	p3.start()


if __name__ == '__main__':
	main()


