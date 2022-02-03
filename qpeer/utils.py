#!/usr/bin/python3

import requests
import re
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
from base64 import b64encode, b64decode
from uuid import uuid4
from errors import *
import os
import time
import random
import hashlib
import socket
import pickle
import struct
import json
import sys
from binascii import hexlify, unhexlify
import pyaes, secrets
import random
import miniupnpc

class Utils:
  def __init__(self):
    self.upnp = miniupnpc.UPnP()
    #Setting RSA key pairs
    if os.path.isfile('privkey.pem'):
      self.key, self.pubkey_pem = self.RSA_read()
    else:
      self.RSA_write()
      self.key, self.pubkey_pem = self.RSA_read()

    #Setting local peer
    if os.path.isfile('lpeer.pkl'):
      self.lpeer = self.read_peers(open('lpeer.pkl','rb'))[0] #Reading lpeer info
      self.peerid = self.lpeer[0]
      self.role = self.lpeer[1]
      self.port = self.lpeer[3]

      if self.lpeer[2] == self.getmyip():
        self.peerip = self.lpeer[2]
      else:
        self.peerip = self.getmyip()
        self.lpeer[2] = self.peerip
        self.write_peers(self.lpeer, open('lpeer.pkl','wb')) #Update file

    else:
      self.peerid = hashlib.sha1(self.pubkey_pem).hexdigest()
      self.port = 1691
      self.peerip = self.getmyip()
      self.role = 0 #Change (1) for hard-coded nodes
      self.lpeer = [self.peerid, self.role, self.peerip, self.port]
      self.write_peers(self.lpeer, open('lpeer.pkl','wb')) #Saving local peer for future use

    #Getting previous peers
    if os.path.isfile('peers.pkl'):
      if len(open('peers.pkl', 'rb').read()) > 1:
        self.peers = self.read_peers()
      else:
        self.peers = list()
    else:
      self.peers = list()

    self.temp_peers = list()
    self.offline_peers = list()

  def getmyip(self):

    upnp = miniupnpc.UPnP()
    self.upnp.discoverdelay = 10
    
    try:
      self.upnp.discover()  
      self.upnp.selectigd()
      ip = self.upnp.externalipaddress()

      return ip
    
    except Exception as e:
      print(e)    

  def RSA_keygen(self): #Generating RSA key pairs
    random_gen = Random.new().read
    key = RSA.generate(2048, random_gen)
    privkey = key.exportKey('PEM')
    pubkey = key.publickey().exportKey('PEM')
    
    return privkey, pubkey

  def RSA_write(self): #Saving RSA key pairs
    privkey, pubkey = self.RSA_keygen()
    
    with open('privkey.pem', 'wb') as privfile:
      privfile.write(privkey)

    with open('pubkey.pem', 'wb') as pubfile:
      pubfile.write(pubkey)

  def RSA_read(self): #Getting RSA key pairs
    with open('privkey.pem', 'rb') as privfile:
      privkey = RSA.importKey(privfile.read())

    with open('pubkey.pem', 'rb') as pubfile:
      pubkey = pubfile.read()

    return privkey, pubkey

  def RSA_encrypt(self, msg, pubkey_pem=None): #Encryption with RSA (penc)
    if pubkey_pem == None:
      pubkey = RSA.importKey(self.pubkey_pem)
      cipher = PKCS1_OAEP.new(pubkey)
      enc_msg = cipher.encrypt(msg)
    else:
      pubkey = RSA.importKey(pubkey_pem)
      cipher = PKCS1_OAEP.new(pubkey)
      enc_msg = cipher.encrypt(msg)
    
    return enc_msg
  
  def RSA_decrypt(self, enc_msg): #Decrytion with RSA (dpenc)
    cipher = PKCS1_OAEP.new(self.key)
    msg = cipher.decrypt(enc_msg)
   
    return msg
  
  def AES_keygen(self): #Generating AES key & iv
    iv = secrets.randbits(256)
    key = hashlib.md5(os.urandom(32)).hexdigest()

    return iv, key.encode()

  def AES_encrypt(self, msg, iv, key): #Encryption with AES (kenc)
    cipher = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
    enc_msg = cipher.encrypt(msg)

    return enc_msg

  def AES_decrypt(self, enc_msg, iv, key): #Decryption with AES (dkenc)
    cipher = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
    msg = cipher.decrypt(enc_msg)

    return msg
  
  def forward_port(self):
    self.upnp.discoverdelay = 10

    try:
      self.upnp.discover()
      self.upnp.selectigd()
      localip = self.upnp.lanaddr
      port = self.port
      r = self.upnp.getspecificportmapping(port, 'TCP')
      while r != None and port < 65536:
        port = port + 1
        r = self.upnp.getspecificportmapping(port, 'TCP')

      forward = self.upnp.addportmapping(port, 'TCP', localip, self.port, 'qPeer port forwarding %u' % port, '')
      return forward

    except Exception as e:
      print(e)

  def close_port(self):
    self.upnp.deleteportmapping(self.port, 'TCP')

  def greet(self):
    msgtype = 'qpeer'
    msg = 'greet'
    payload = struct.pack('<40s5s', self.peerid.encode(), msg.encode())

    return json.dumps((msgtype,payload))

  def unpack_greet(self, payload):
    unpack_payload = struct.unpack('<40s5s', payload)

    return unpack_payload

  def bye(self):
    msg = 'bye'
    return msg.encode()

  def ping(self):
    msg = 'ping'
    return msg.encode()

  #Setting up secure connection & Exchanging RSA & AES keys
  
  def init(self): 
    payload = struct.pack('<40s600s', self.peerid.encode(), b64encode(self.pubkey_pem))
    return payload

  def unpack_init(self, payload):
    info = struct.unpack('<40s600s', payload)
    return info

  def penc_AES(self, key, iv, pubkey_pem):
    penc_AES_key = self.RSA_encrypt(b64encode(f'{iv}:{key.decode()}'.encode()), pubkey_pem)
    
    return b64encode(penc_AES_key)

  def dpenc_AES(self, payload):
    dec_msg = self.RSA_decrypt(b64decode(payload))
    iv,key = str(b64decode(dec_msg).decode()).split(':')
    
    return iv,key

  def pack_ip(self):
    return socket.inet_aton(self.peerip)

  def unpack_ip(self, payload):
    return socket.inet_ntoa(payload)

  #Exchaning peerinfo

  def peerinfo(self):
    payload = struct.pack('<i4sh600s',self.role,self.pack_ip(),self.port,b64encode(self.pubkey_pem))
    
    return payload

  def kenc_peerinfo(self, AES_iv, AES_key):
    enc_payload = self.AES_encrypt(self.peerinfo(), AES_iv, AES_key)
    
    return b64encode(enc_payload)

  def unpack_peerinfo(self, payload): 
    un_peerinfo = [info for info in struct.unpack('<i4sh600s', payload)]
    un_peerinfo[1] = self.unpack_ip(un_peerinfo[1])
    
    return un_peerinfo

  def handle_peerinfo(self, payload):
    peerinfo = []

    for info in self.unpack_peerinfo(payload):
      if type(info) == bytes:
        peerinfo.append(info.decode())
      else:
        peerinfo.append(info)

    return peerinfo

  def dkenc_peerinfo(self, payload, AES_iv, AES_key):
    dec_payload = self.AES_decrypt(b64decode(payload), AES_iv, AES_key)
    
    return self.handle_peerinfo(dec_payload)

  #Saving all peer info
  def save_lpeer(self,peerid,peerinfo,iv,key): 
    enc_peerinfo = self.AES_encrypt(json.dumps(peerinfo),int(iv),key)
    enc_key = self.RSA_encrypt(key)
    peer = [peerid, b64encode(enc_peerinfo).decode(),iv,b64encode(enc_key).decode()]
    if self.check_peer(peerid) == False:
      self.peers.append(peer)
      self.write_peers(peer)
    else:
      raise LpeerError
      pass

  def write_peers(self, peer, file=open('peers.pkl', 'ab')): #Save peers to a file
    pickle.dump(peer, file)

  def read_peers(self,file=open('peers.pkl', 'rb')): #Read peers from file 
    peers = [pickle.load(file)]
    return peers

  def find_peer(self,peerid,peerlist=None): #Return Peer by peerid
    if peerlist == None:
      for peer in self.peers:
        if peer[0] == peerid:
          return peer
          break
        else:
          continue
    else:
      for peer in peerlist:
        if peer[0] == peerid:
          return peer
          break
        else:
          continue


  def decrypt_key(self, peer): #Decrypting AES key (dpenc)
    enc_key = peer[-1]
    key = self.RSA_decrypt(b64decode(enc_key))
    
    return key

  def decrypt_peerinfo(self, key, peer): #Decrypting peerinfo (dkenc)
    enc_peerinfo = peer[1] 
    peerinfo = self.AES_decrypt(b64decode(enc_peerinfo),int(peer[2]),key)
    return json.loads(peerinfo)

  def decrypt_peer(self, peerid, peerlist=None): #Returning all peer info
    enc_peer = self.find_peer(peerid, peerlist)
    peerid = enc_peer[0]
    iv = enc_peer[2]
    key = self.decrypt_key(enc_peer)
    peerinfo = self.decrypt_peerinfo(key, enc_peer)

    return [peerid, peerinfo, iv, key]

  def return_temp_peer(self, peerid): #Sending specific peer info for peer discovery
    peer = self.decrypt_peer(peerid)
    peerinfo = peer[1]
    ip, port = peerinfo[1:3]

    return [peerid, ip, port]

  def remove_peer(self, peerid): #If peer does not respond
    if self.check_peer(peerid) == True and self.check_peer(peerid, self.offline_peers) == False:
      del_peer = self.find_peer(peerid,self.peers)
      peers = self.read_peers()
      peers.remove(del_peer)

      if len(peers) > 0:
        for peer in peers:
          self.write_peers(peer)
      else:
        file = open('peers.pkl', 'wb')
        self.write_peers(peers, file)

      self.offline_peers.append(self.return_temp_peer(peerid))
      self.peers.remove(del_peer)
    else:
      pass

  def getback_peer(self, peerid): #If peer responds and it was offline
    if self.check_peer(peerid, self.offline_peers) == True and self.check_peer(peerid) == False:
      peer = self.find_peer(peerid,self.offline_peers)
      self.offline_peers.remove(peer)
      self.temp_peers.append(peer)
    else:
      pass

  def check_peer(self, peerid, peerlist=None): #Check if peer already exists
    if peerlist == None:
      return any(peerid in peer for peer in self.peers)
    else:
      return any(peerid in peer for peer in peerlist)
    
  def return_peers(self):
    peers = []
    if len(self.peers) <= 5:
      for peer in self.peers:
        peerid = peer[0]
        temp_peer = self.return_temp_peer(peerid)
        peers.append(temp_peer)
    else:
      for i in range(5):
          peer = random.choice(self.peers)[:-2]
          if peer not in peers:
            peerid = peer[0]
            temp_peer = self.return_temp_peer(peerid)
            peers.append(temp_peer)
          else:
            pass
    return peers

  #Exchaning peers
  def share_peers(self,iv,key): 
    jsonized = json.dumps(self.return_peers())
    payload = b64encode(self.AES_encrypt(jsonized.encode(), iv, key))

    return payload

  def save_peers(self,payload,iv,key): 
    un_payload = b64decode(payload)
    peers = json.loads(self.AES_decrypt(un_payload, iv, key).decode())
    for peer in peers:
      if peer[0] == self.peerid and peer[1] == self.peerip: #Check if the peer is me 
        if self.check_peer(peer[0]) == False and self.check_peer(peer[0],self.temp_peers) == False and self.check_peer(peer[0], self.offline_peers) == False: #Check if peer already exists
          self.temp_peers.append(peer)
        else:
          raise PeersError
          pass
      else:
        raise IdError
        pass

  
