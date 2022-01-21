import sys
sys.path.insert(1, 'qpeer')
from node import *
from errors import *
from multiprocessing import Process
import socket
import _thread
import random

server = Server()
def run_server():
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.bind(('', 1691))
	soc.listen(10)

	while True:
		conn, addr = soc.accept()
		try:
			_thread.start_new_thread(server.setup, (conn, ))
		except Exception as e:
			print(e)

client = Client()

def run_client():		
	if len(client.peers) > 0:
		
		if len(client.temp_peers) > 0:
			peer = random.choice(client.temp_peers)
			print(peer)
			try:
				client.setup(peer[1], peer[2])
				client.temp_peers.remove(peer)
			except socket.error:
				client.temp_peers.remove(peer)
				client.offline_peers.append(peer)
			except Exception as e:
				print(e)
		else:
			peer = utils.decrypt_peer(random.choice(client.peers)[0])
			peerinfo = peer[1]
			try:
				client.setup(peerinfo[1], peerinfo[2])
			except socket.error:
				print(e)

	else: #Bootstrap
		ip = '' #Set the supernode ip
		port = 1691
		try:
			client.setup(ip, port)
		except Exception as e:
			print(e)

		

if __name__ == '__main__':
	"""print("Clt Running")
				run_client()
				print("Peers\n")
				print(client.peers)
				print("Temp Peers\n")
				print(client.temp_peers)"""
	print("Srv running")
	run_server()


