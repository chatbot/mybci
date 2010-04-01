import sys 
sys.path.append('..')

from network.EEGTransport import *

x = EEGTransport('udp_m_serv', '224.0.0.1', 17000)

for i in xrange(4):
	data = x.recvChunked()
	header = x.getTransportHeader()
	#print 'packet: ' + str(header.getNum()) + ' chunks: ' + str(header.getChunks()) + '\n'
	#print 'header: ' + header.getEEGHeader().get_header()
	sys.stderr.write('Packet: ' + str(i))
	print data
	
x.close()