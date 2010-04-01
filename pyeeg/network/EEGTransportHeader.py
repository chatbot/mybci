import struct
from common.EEGHeader import *

class EEGTransportHeaderException:
	pass

class EEGTransportHeader:
		
	# num(4) chunks(4) chunk(4) hash(4) size(4) [ n-channels: 26, n-points: 250, frequency: 5000, type:  uint32] [data]
	
	
	__fmt = 'IIIII'
	
	def __init__(self):
		self.__hash = 0
		self.__num = 0
		self.__chunk = 0
		self.__chunks = 0
		self.__update = True
		self.__eeghead = EEGHeader()
		self.__fullheadlen = 0
	
	def setNum(self, num):
		self.__num = num
	
	def getNum(self):
		return self.__num
	
	def setChunk(self, ch):
		self.__chunk = ch
		
	def getChunk(self):
		return self.__chunk
		
	def setChunks(self, ch):
		self.__chunks = ch
		
	def getChunks(self):
		return self.__chunks
		
	def __calchash(self, header):
		self.__hash = 0
		lsym = '\x00'
		for sym in header:			
			self.__hash += ord(lsym) ^ ord(sym)
			lsym = sym
	
	def getHash(self):
		return self.__hash
		
	def setEEGHeader(self, h):
		self.__eeghead.set_header(h)
	
	def getEEGHeader(self):
		return self.__eeghead
		
	def getFullHeaderLen(self):
		return self.__fullheadlen
		
	def getTransportHeader(self):	
		if self.__update: # static header part
			self.__calchash(self.__eeghead.get_header())			
			self.__eegheadlen = len(self.__eeghead.get_header())			
			self._update = False
			
		self.__header = struct.pack(self.__fmt, self.__num, self.__chunks, self.__chunk, self.__hash, self.__eegheadlen) 
		return self.__header + self.__eeghead.get_header()
	
	def setTransportHeader(self, header):		
		size = struct.calcsize(self.__fmt)
		
		if len(header) < size:
			if __debug__:
				print 'Header length too small'
			self.__init__()
		
		self.__num, self.__chunks, self.__chunk, self.__hash, self.__eegheadlen = struct.unpack(self.__fmt, header[:size])
		
		if self.__eegheadlen == 0:
			if __debug__:
				print 'EEGHeader is empty'
		
		if len(header) < size + self.__eegheadlen:
			raise EEGTransportHeaderException, 'Header length too small'			
			self.__init__()
			
		self.__fullheadlen = size + self.__eegheadlen 
		self.__eeghead.set_header(header[size:self.__fullheadlen])
	