one):
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
		sleep = core.time.sleep_us
		self.recv.irq(trigger = 0,handler = None)
		sleep(1000)
		for x in range(length):
			duty(512 if x%2==0 else 0)
			sleep(packet[x]*50)
		duty(0)
		sleep(3000)
		self._recvActive(True)
	
	