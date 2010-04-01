# Echo client program
import socket,sys

HOST = 'localhost'    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
#/data = s.recv(1024)
while True:
    s.send(open('fft/ffts.bin',"rb").read())
    sys.stdin.readline()

s.close()
