import socket
#import json
from errors import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 1337
s.connect((host, port))

def send(msg):
  s.send(bytes(msg.encode()))
  print(s.recv(8192))
  #s.close()
