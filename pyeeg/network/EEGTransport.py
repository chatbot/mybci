from socket import *
from EEGTransportHeader import *
import struct
import sys
from numpy import *
import bz2


class EEGTransportException:
	pass

class EEGFmtChangedException:
	pass

class EEGTransport:
	'Class for creation data connections sockets.'
	
	__types = ['tcp_cl', 'tcp_serv', 'udp_m_cl', 'udp_m_serv']
	
	__chunk_size = 768
	
	def __init__(self, type, addr='0.0.0.0', port=0):
		
		self.__addr = addr
		self.__port = port
		self.__hash = None
		
		self.__thead = EEGTransportHeader() 
		
		self.__num = 1
		
		self.__type = type
		
		if isinstance(type, socket):
			if __debug__:
				print 'Accepted socket.'
			self.__eegsocket = type			
		else:						
			if type not in self.__types:
				raise EEGTransportException('Unknown socket type')			
			
			if type=='tcp_serv':
				self.__eegsocket = socket(AF_INET, SOCK_STREAM)
				self.__eegsocket.bind( (addr, port) )
				self.__eegsocket.listen(10)
			
			if type=='tcp_cl':
				self.__eegsocket = socket(AF_INET, SOCK_STREAM)   
				self.__eegsocket.connect( (addr, port) )				
				
			if type=='udp_m_serv':
				self.__eegsocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)   
				self.__eegsocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
				self.__eegsocket.bind( ('', port) )
				
				mreq = struct.pack('4sl', inet_aton(addr), INADDR_ANY)
				
				self.__eegsocket.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)
				
			if type=='udp_m_cl':
				self.__eegsocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
				self.__eegsocket.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, 2)
				
	
	def accept(self):
		if self.__type == 'udm_m_serv' or self.__type == 'udp_m_cl':
			raise EEGTransportException('Unsupported method "accept" for this type of connection')
		newsock, newaddr = self.__eegsocket.accept()
		newconn = EEGTransport(newsock, newaddr)
		return newconn
		
	def __recv(self, count):
                return self.__eegsocket.recv(count)
                
#                l=[]
#                torecv = count
#                while (torecv > 0) {
#                        d = self.__eegsocket.recv(torecv)
#                        l.append(d)
#                        torecv = torecv - len(d)
#                }
#                return ''.join(l)
		
	def __send(self, data):
		if self.__type == 'udm_m_serv' or self.__type == 'udp_m_cl':
				self.__eegsocket.sendto(data, (self.__addr, self.__port))
		elif self.__type == 'tcp_serv' or self.__type == 'tcp_cl':
			self.__eegsocket.send(data)
			
	def close(self):
		self.__eegsocket.close()
		
	def getTransportHeader(self):
		return self.__thead
	
	def getData(self):
		pass

	def sendChunked(self, data):
                print 'orig size: ',len(data),
                data=bz2.compress(data,6)
                print 'compressed: ',len(data)
		header = self.__thead.getTransportHeader()		
		hlen = len(header)
		dlen = len(data)
		dchunk = self.__chunk_size - hlen
		count =  dlen/ dchunk
		
		if dlen % self.__chunk_size > 0:
			count+=1			
			
		for i in xrange(count):
			# if __debug__:
			# 	print 'packet: ' + str(self.__num) + ' chunks: ' + str(count) + ' chunk: ' + str(i) + '\n'
			self.__thead.setNum(self.__num)
			self.__thead.setChunks(count)
			self.__thead.setChunk(i)
			header = self.__thead.getTransportHeader()
			self.__send(header + data[(dchunk*i):(dchunk*i + dchunk)])
		self.__num += 1


        def recvData(self):        
		wait_for_chunk = 0	
		data = []
		while self.__thead.getChunks() == 0 or wait_for_chunk < self.__thead.getChunks():
			chunk = self.__recv(self.__chunk_size)
			self.__thead.setTransportHeader(chunk)
			
			if self.__hash != self.__thead.getHash():
				if self.__hash == None:
					self.__hash = self.__thead.getHash()
				else:
                                        self.__hash = self.__thead.getHash()
					raise EEGFmtChangedException#('EEGData format changed')
			
			if wait_for_chunk != self.__thead.getChunk():
				if __debug__:
					sys.stderr.write('skipping packet: ' + str(self.__num)\
                                                         + ' chunk: ' + str(self.__thead.getChunk()) + '\n')
				wait_for_chunk = 0
				data = []
			data.append(chunk[self.__thead.getFullHeaderLen():])	
			wait_for_chunk += 1
			self.__num = self.__thead.getNum()

		#return concatenate(data)	
		return  ''.join(data)

	def recvChunked(self):
                #print 'compressed size: ',len(data),
                while(True):
                        data = self.recvData() 
                        try:
                		orig = bz2.decompress(data)
                	except:
                                sys.stderr.write('Decompress error, skipping \
                                                packet: ' + str(self.__num) +'\n')
                        else:
                                header = self.__thead.getEEGHeader()					
                                size = header.n_channels * header.n_points * 4
                                if size != len(orig):
                                        sys.stderr.write('Wrong size of packet:' + str(len(orig)) +\
                                                         'must be ' + str(size) + '\n')
                                else:        
                                        break
                #print 'orig size: ',len(orig)
                return orig

