import sys 
sys.path.append('..')

from network.EEGTransport import *

x = EEGTransport('tcp_serv', 'localhost', 999)

x = x.accept()


while 1:
        data = x.recv(10)
	if data:
		print data
	else:
		break
		
x.close()