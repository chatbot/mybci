import struct

class EEGHeader:
	
	data_types = {'float32':float, 'int32':int}
	
	
	def __init__(self):
		
		self.__params = {}
		
		self.n_channels = None
		self.n_points = None
		self.n_blocks = None
		self.frequency = None
		self.type = None
		self.names= None
		
		self.__params['n-channels:'] = self.__n_channels
		self.__params['n-points:'] = self.__n_points
		self.__params['n-blocks:'] = self.__n_blocks
		self.__params['frequency:'] = self.__frequency
		self.__params['type:'] = self.__type
		self.__params['names:'] = self.__names
		
	def set_header(self, header):
		#check header type		
		s = header.split(',')		
		for param in s:
			s_param = param.split()
			if self.__params.has_key(s_param[0]):
				#print 'key: "%s" value: "%s" ' % (s_param[0],s_param[1] )
				#print  self.__params[s_param[0]]
				setter = self.__params[s_param[0]]
				setter(s_param[1])
	def get_header(self):
		s = ''
		for key in self.__params.keys():						
			getval = self.__params[key]
			val = getval()
			if val:
				if len(s) > 0:
					s += ', '
				s += key + ' ' + str(val)
		return s


	#param setters
	def __n_channels(self, val=None):
		if val: 
			self.n_channels = int(val)
		return self.n_channels
	def __n_points(self, val=None):
		if val: 
			self.n_points = int(val)
		return self.n_points
	def __n_blocks(self, val=None):
		if val:
			self.n_blocks = int(val)
		return self.n_blocks
	def __frequency(self, val=None):
		if val:
			self.frequency = int(val)
		return self.frequency
	def __type(self, val=None):
		if val:
			self.type = val
		return self.type
	def __names(self, val=None):
		if val:
			self.names = val
		return self.names

if __name__ == '__main__':
	h = EEGHeader ()
	h.set_header('n-channels: 26, n-points: 250, frequency: 5000, type:  uint32')
	print h.n_channels,  h.n_points,  h.n_blocks, h.frequency, h.type
	print h.get_header()
	
