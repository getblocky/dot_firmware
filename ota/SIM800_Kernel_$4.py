e
		while self._liEvent[data] == None :
			await asyncio.sleep_ms(10)
		return self._liEvent.pop(data)
		
	async def write(self,data):
		data = bytes(data,'utf-8') if isinstance(data,str) else data
		self.echo = data.strip()
		try :
			temp=self.uart.read();self.buffer+=temp;self.debugport.write(b'>>>'+temp)
		except :
			pass
		if len(self.buffer):
			print('\t\t[DUMPING]\t\t' , self.buffer)
			self.parsing()
		self.uart.write(data)
		self.debugport.write(data)
		print('\t\t[WRITE]\t\t',data)
		
	async def waitReady(self):
		return
		while self.running == True :
			await asyncio.sleep_ms(1)
		self.running = True
		self.polling = True
		while True :
			if len(self.buffer):
				self.parsing()
			await self.write(b'AT\r\n')
			await asyncio.sleep_ms(100)
			if self.uart.any() > 0:
				temp=self.uart.read();self.buffer+=temp;self.debugport.write(b'>>>'+temp)
				print('\t\t[READY]\t\t' , end = '')
				if b'OK' in self.buffer:
					self.polling = False
					self.running = False
					return
				self.parsing()
		
			
	
	# ================ Application API ===================#
	async def gprs(self,state):
		if state == True :
			r = await self.request('+CFUN?')
			if r[0] != 1 :
				await self.command('+CFUN=1')
			r = await self.request('+CGATT?')
			if r[0] != 1 :
				await self.command('+CGATT=1')
			await self.command('+SAPBR=3,1,"Contype","GPRS"')
			await self.command('+SAPBR=3,1,"APN","v-internet"')
			await self.command('+CGDCONT=1,"IP","v-internet"')
			await self.command('+CGACT=1,1')
			await self.command('+SAPBR=1,1')
			await self.request('+SAPBR=2,1',prefix = '+SAPBR:')
			await self.command('+CGATT=1')
			await self.command('+CIPMUX=1')
			await self.command('+CIPQSEND=1')
			await self.command('+CIPRXGET=1')
			await self.command('+CSTT="v-internet"')
			await self.command('+CIICR')
			await self.request('+CIFSR',prefix = b'*')
			
			#await self.command('+CMEE=2')
			#await self.command('+CIFSR;E0',prefix = '11.185.172.8')
			await self.command('+CDNSCFG="2