txt".format(name) in core.os.listdir("IR"):
			return True
		return False

	def _recognise(self , bin):
		for x in self.event_list :
			if self.event_list[x]["bin"] == bin :
				return x
		return None

	def _decode(self , packet = None, length = None):
		binary = 0
		m = 500000
		if length == None and packet == None :
			length = self.length
			packet = self.buffer
		else :
			length = length or len(packet)
		for x in range(length):
			m = min(packet[x] , m)
		for x in range(0 , length , 2):
			if packet[x+1] > packet[x]*2 :
				binary += 2**(x//2)
		return binary


	# User exposed function


	def event (self , name , function):
		if self._learned(name):
			self.event_list[name] = [self._load(name)]

	def send ( self , name , length = None):
		self._recvActive(False)
		packet = []
		length = 0

		if isinstance(name , str):
			length , _ ,	packet = self._load(name,True)
		if isinstance(name , bytearray):
			length = length or len(name)
			packet = name
		duty = self.pwm.duty
		sleep = c