onselist:
					self.responselist = self.responselist.index(cmd)
					#print('<recv> Reponse = {}'.format(self.responselist))
				elif cmd in self.waitinglist:
					if cmd in self.waitinglist : # Damn you CIFSR
						self.waitinglist.remove(cmd)
						self.dict[cmd] = ans
						if len(data):
							data = data[0:-5]
							self.dict[cmd].append(data)
					else :
						print('No prefix' , self.echo, cmd)
				else :
					prefix = self.echo[2:-3]
					if prefix in self.waitinglist:
						self.waitinglist.remove(prefix)
					self.dict[prefix] = cmd
					#print('<recv> Request = {}'.format(self.dict[cmd]))
				self.buf = b''
				
			if self.uart.any() > 0:
				self.buf = self.uart.read()
	async def sendSMS(self,number,message):
		#print('Sending SMS to ', number)
		await self.command('+CMGF=1')
		await self.command('+CSCS="GSM"')
		await self.command('+CMGS="{}"'.format(number),prefix=['>'])
		#print('Message = ',message)
		self.uart.write(message)
		self.uart.write(bytearray([0x1A]))
		#print('Done')
	async def http(self,link):
		r = await self.request('+CFUN?')
		if r[0] == 1:
			print('CFUN Ready')
		r = await self.request('+CGATT?')
		if r[0] == 1:
			print('CGATT Ready')
		await self.command('+SAPBR=3,1,"Contype","GPRS"')
		await self.command('+SAPBR=3,1,"APN","v-internet"')
		await self.command('+SAPBR=1,1')
		await self.command('+HTTPINIT')
		await self.command('+HTTPPARA="URL","{}"'.format(link))
		await self.command('+HTTPPARA="CID",1'.format(link))
		r = await self.request('+HTTPACTION=0'.format(link))
		#print('HTTP Received' , r)
		r = await self.request('+HTTPREAD')
		#print('====Content======')
		#print(r)
		#print('=================')
		
	# What blynk need :)
	def __repr__(self):
		print('WaitingList = ' , self.waitinglist)
		print('ResponseList = ' , self.responselist)
		print('Dictionary = ' , self.dict)
		print('EchoEcho = ' , self.echo)
	async def settimeout(self,timeout):
		print('[SIM800] Set Timeout = {}'.format(timeout))
	async def recv(self,size):
