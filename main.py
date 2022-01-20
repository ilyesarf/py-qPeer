import sys
sys.path.insert(1, 'qpeer')
from node import *
from errors import *
from multiprocessing import Process
import socket
import _thread

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
	host = '172.17.0.1'
	port = 1691
	try:
		client.setup(host, port)
	except Exception as e:
		print(e)

if __name__ == '__main__':
	print("Clt Running")
	run_client()
	print("Peers\n")
	print(client.peers)
	print("Temp Peers\n")
	print(client.temp_peers)
	print("Srv running")
	run_server()


#TODO: If there's no peers in temp_peers nor peers, start with bootstrap node. Else, pick random peer.
