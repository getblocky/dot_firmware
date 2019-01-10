mmand(self,data,response = [b"OK",b"ERROR"]):
		await self.waitReady()
		while self.running == True :
			await asyncio.sleep_ms(10)
		self.running = True
		data = bytes(data,'utf-8') if isinstance(data,str) else data
		self._liCommand = response
		
		
		await self.write(b'AT' + data + b'\r\n')
		self.polling = True
		while not isinstance(self._liCommand,int) :
			
			self.parsing()
			while self.uart.any() == 0:
				await asyncio.sleep_ms(1)
			while self.uart.any() > 0 :
				temp = self.uart.read()
				self.buffer += temp
				self.debugport.write(b'>>>' + temp)
				await asyncio.sleep_ms(1)
			self.parsing()
		self.polling = False
		
		self.running = False
		return self._liCommand
	
	async def routine(self):
		# this is purely to polling for _jEvent
		while True :
			await asyncio.sleep_ms(10)
			if self.polling == False and self.uart.any():
				temp = self.uart.read()
				
				self.buffer += temp
				self.debugport.write(b'>>>' + temp)
				self.parsing()
		
	async def request(self,data,prefix = None):
		await self.waitReady()
		while self.running == True :
			await asyncio.sleep_ms(10)
		self.running = True
		data = bytes(data,'utf-8') if isinstance(data,str) else data
		if prefix == None :
			prefix = b''
			for x in range(len(data)):
				if data[x:x+1] in [b' ',b'+',b','] or data[x:x+1].isalpha() or data[x:x+1].isdigit():
					prefix += data[x:x+1]
			self._liRequest = prefix
		else:
			self._liRequest = prefix
		
		
		await self.write(b'AT' + data + b'\r\n')
		self.polling = True
		while isinstance(self._liRequest,bytes) :
			self.parsing()
			while self.uart.any() == 0:
				await asyncio.sleep_ms(1)
			while self.uart.any() > 0 :
				temp=self.uart.read();self.buffer+=temp;self.debugport.write(b'>>>'+temp)
				await asyncio.sleep_ms(1)
			self.parsing()
		self.running = False
		self.polling = False
		return self._liRequest
		
	async def waitfor(self,data,timeout = 1000):
		data = bytes(data,'utf-8') if isinstance(data,str) else data
		self._liEvent[data] = Non