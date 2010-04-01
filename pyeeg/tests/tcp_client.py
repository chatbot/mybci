import sys 
sys.path.append('..')

from network.EEGTransport import *

x = EEGTransport('tcp_cl', 'localhost', 999);

for i in xrange(100):
	x.send('%i' % i)
x.close()