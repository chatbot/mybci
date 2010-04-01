import sys 
import time
sys.path.append('..')

from network.EEGTransport import *

x = EEGTransport('udp_m_cl', '224.0.0.1', 17000)

data = ''

len =100000
x.getTransportHeader().setEEGHeader('n-points: 250,frequency: 5000, type: uint32,names: a b c d e f')

for i in xrange(4):
	for c in xrange(len):
			data += str(c) +','
	x.sendChunked(data)
	print data
	time.sleep(1)
x.close()