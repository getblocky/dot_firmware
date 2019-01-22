self._liRequest != None :
			print('[request]' , self._liRequest)
		if self._liEvent != None :
			print('[event]' , self._liEvent)
		if self._string != None :
			print('[parsestring]' , self._string)
		print('polling = ' , self.polling , 'running = ' , self.running)
		return ''
	async def routine(self):
		while True:
			await asyncio.sleep_ms(10)
			if self.polling == False and self.uart.any() > 0:
				while self.uart.any() > 0 :
					self.buffer += self.uart.read()
					await asyncio.sleep_ms(1)
				self.parsing()

	async def request(self,data, prefix=None,timeout = 1000):
		# claiming the control
		while self.running == True:
			await asyncio.sleep_ms(10)
		self.running = True
		if isinstance(data,str):
			data = bytes(data,'utf-8')
		elif isinstance(data,bytes):
			data = data
		elif isinstance(data,bytearray):
			data = bytes(data)
		else :
			return

		# generate prefix string
		if prefix == None:
			prefix = b''
			for x in range(len(data)):
				if data[x:x+1] in [b' ',b'+',b',']