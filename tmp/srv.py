import socket
import test
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 1337

s.bind((host, port))
s.listen(5)
conn, addr = s.accept()

while True: 
  try:
    recvd = conn.recv(2048)
    print(recvd)
    conn.send(bytes('Ok'.encode()))
  except Exception as e:
    print(e)
    s.close()
    break
