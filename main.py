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
			firstmsg = conn.recv(2048)
			if firstmsg[0] == 'qpeer': #Check msgtype
				_thread.start_new_thread(server.setup, (conn, firstmsg[1],))
			else:
				pass
		except Exception as e:
			print(e)

			


client = Client()

def run_client():
	while True:
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
					pass
			else:
				peer = utils.decrypt_peer(random.choice(client.peers))
				peerinfo = peer[1]
				if peerinfo[0] == 0
					try:
						client.setup(peerinfo[1], peerinfo[2])
					except socket.error:
						utils.remove_peer(peer[0])
					except Exception as e:
						print(e)
						pass
				else:
					pass
					
		else: #Bootstrap
			ip = '' #Set the supernode ip (hard-coded node)
			port = 1691
			try:
				client.setup(ip, port)
			except Exception as e:
				print(e)

def ping_client():
	while True:
		if len(client.peers) > 1:
			peer = random.choice(client.peers)		
			client.ping(peer[0])
		else:
			pass

def getback_client():
	while True:
		if len(client.offline_peers) > 0:
			peer = random.choice(client.offline_peers)
			client.getback_client(peer[0])
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

	p4 = Process(target=ping_client)
	p4.start()

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
		main()


