#!/usr/bin/python3

from errors import *
import socket
import utils
import struct
import hashlib
from base64 import b64encode, b64decode

utils = utils.Utils()

class Client:
	def __init__(self):
		self.peers = utils.peers
		self.temp_peers = utils.temp_peers
		self.offline_peers = utils.offline_peers		

	def setup(self,peerip,peerport):
		soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		soc.connect((peerip,peerport))
		
		def greet():
			msg = utils.greet()
			soc.send(msg)
			recvd = soc.recv(2048)
			if recvd:
				return recvd
			else:
				raise InitError
				soc.close()

		def handle_greet():
			msg_greet = utils.unpack_init(greet())
			return msg_greet[0],b64decode(msg_greet[1])

		peerid, pubkey_pem = handle_greet()
		
		if peerid.decode() == hashlib.md5(pubkey_pem).hexdigest():
			pass
		else:
			raise IdError
			soc.close()


		AES_iv, AES_key = utils.AES_keygen()

		def send_key():
			soc.send(utils.penc_AES(AES_key,int(AES_iv),pubkey_pem))
			recvd = soc.recv(2048)
			if recvd:
				return recvd
			else:
				raise PeerinfoError
				soc.close()

		peerinfo = utils.dkenc_peerinfo(send_key(), AES_iv, AES_key)
		try:
			utils.save_lpeer(str(peerid.decode()),peerinfo,AES_iv,AES_key)
		except LpeerError:
			print('[!] Peer already exists')
			soc.close()

		def send_peerinfo():
			payload = utils.kenc_peerinfo(int(AES_iv), AES_key)
			soc.send(payload)
			recvd = soc.recv(8192)
			if recvd:
				return recvd
			else:
				raise PeersError
				soc.close()

		peers = send_peerinfo()
		try:
			utils.save_peers(peers, int(AES_iv), AES_key)
		except Exception as e:
			print(e)
			soc.close()

		def send_peers():
			payload = utils.share_peers(int(AES_iv), AES_key)
			soc.send(payload)
			recvd = soc.recv(2048)
			if recvd == utils.bye():
				soc.close()
			else:
				raise ByeError
				soc.close()

		def send_bye():
			if len(self.peers) <= 5:
				soc.send(utils.bye())
				soc.close()
			else:
				send_peers()
				soc.close()
		send_bye()

	def ping(self, peerid,peerlist=None):
			peer = utils.find_peer(peerid, peerlist)
			peerinfo = utils.decrypt_peer(peer[0])[1]
			ip, port = peerinfo[1:3]
			
			soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			
			try:
				soc.connect((ip,port))
				soc.close()
			except socket.error:
				utils.remove_peer(peer[0])


class Server:
	def __init__(self):
		self.peers = utils.peers
		self.temp_peers = utils.temp_peers
		self.offline_peers = utils.offline_peers
		# self.connected_peers = [] Important?

	#TODO: Rewrite this while focusing on handling multiple peers at one time.
	#Harder than i thought
	def setup(self, conn):

		def greet():
			msg = conn.recv(1024)
			unpack_msg = utils.unpack_greet(msg)
			if len(unpack_msg) == 2 and str(unpack_msg[1].decode()) == 'greet':
				peerid = unpack_msg[0]
				return str(peerid.decode())
			else:
				raise GreetError
				conn.close()
		
		peerid = greet()

		def init():
			conn.send(utils.init())
			recvd = conn.recv(2048)
			if recvd:
				return recvd
			else:
				raise AesError
				conn.close()

		AES_iv, AES_key = utils.dpenc_AES(init())

		def send_peerinfo():
			conn.send(utils.kenc_peerinfo(int(AES_iv), AES_key.encode()))
			recvd = conn.recv(2048)
			if recvd:
				return recvd
			else:
				raise PeerinfoError
				conn.close()

		peerinfo = utils.dkenc_peerinfo(send_peerinfo(), int(AES_iv), AES_key.encode())
		if peerid == hashlib.md5(b64decode(peerinfo[-1])).hexdigest():
			pass
		else:
			raise IdError
			conn.close()
		
		try:
			utils.save_lpeer(peerid, peerinfo, AES_iv, AES_key.encode())
		except LpeerError:
			print("[!] Peer already exists")
			conn.close()

		def send_peers():
			conn.send(utils.share_peers(int(AES_iv), AES_key.encode()))
			recvd = conn.recv(8192)
			if recvd != utils.bye() and len(recvd) > 0:
				try:
					utils.save_peers(recvd, int(AES_iv), AES_key.encode())
					conn.close()
				except Exception as e:
					print(e)
					conn.close()
			else:
				conn.send(utils.bye())
				conn.close()
		
		send_peers()
		print("Done")
