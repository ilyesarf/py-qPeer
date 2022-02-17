#!/usr/bin/env python3

import sys
sys.path.insert(1, 'qpeer')
from node import Server, Client
from errors import *
from utils import Utils
utils = Utils()
import socket
import threading
import random
import time
import requests
import os

server = Server()


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
					firstmsg = utils.unpack_qpeer(conn.recv(2048))
					if firstmsg[0].decode() == 'setup': #Check msgtype
						threading.Thread(target=server.setup, args=(conn, firstmsg[1].decode(),)).start()
					elif firstmsg[0].decode() == 'exchange_peers' and utils.check_peer(firstmsg[1].decode()) == True:
						threading.Thread(targe=server.exchange_peers, args=(conn, firstmsg[1].decode())).start()
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

client = Client()

def run_client():
	if len(client.peers['peers']) > 0:
		if len(client.temp_peers) > 0:
			peer = random.choice(client.temp_peers)
			try:
				client.setup(peer['peerip'], peer['port'])
				client.temp_peers.remove(peer)
			except socket.error:
				client.temp_peers.remove(peer)
				client.offline_peers.append(peer)
			except Exception as e:
				print(e)
				pass
		else:
			enc_peer = random.choice(client.peers['peers'])
			peer = utils.decrypt_peer(enc_peer['peerid'])
			peerinfo = peer['peerinfo']
			if peerinfo[0] == 0:
				try:
					client.setup(peerinfo[1], peerinfo[2])
				except socket.error:
					utils.remove_peer(peer['peerid'])
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
	if len(client.peers['peers']) > 1:
		peer = random.choice(client.peers)
		client.ping(peer['peerid'])
	else:
		pass

def getback_client():
	if len(client.offline_peers) > 0:
		peer = random.choice(client.offline_peers)
		client.getback(peer['peerid'])
	else:
		pass

def main():

	threading.Thread(target=run_server).start()
	threading.Thread(target=run_client).start()
	threading.Thread(target=ping_client).start()
	threading.Thread(target=getback_client).start()

def internet_check():
	while True:
		try:
			time.sleep(2)
			req = requests.get('https://google.com', timeout=3)
			return True
		except Exception as e:
			print(e)
			return False

if __name__ == '__main__':
	while internet_check() == True:
		main()
	else:
		print("No internet access")
		sys.exit()
