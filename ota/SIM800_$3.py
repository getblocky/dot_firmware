),prefix=['>'])
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
		print('[SIM800] Perform Receiving')
		buf = b''
		availalbe  = 0
		received  = 0
		r = await self.request('+CIPRXGET=2,2,{}'.format(size))
		received += r[2]
		if received == size :
			print('#'*50)
			print('[RECEIVED] ,' ,r[4])
			return r[4]
			
		for x in range(10) :
			a = await self.request('+CIPRXGET=4,2')
			if a == [1,1] :
				continue 
			if a[2] != 0 :
				temp = await self.request('+CIPRXGET=2,2,{}'.format(a[2]))
				received += temp[2]
				buf += temp[4]
				if received >= size :
					print('#'*50)
					print('[RECEIVED] ,' ,buf)
					return buf
			else :
				await asyncio.sleep_ms(200)
		return buf
		
	async def send(self,data):
		print('[SIM800] Sending' , data)
		await self.command('+CIPSEND=2,{}'.format(len(data)),prefix=['>'])
		print('[SIM800] Sending Package = ' , data,end='')
		print('Sent' , self.uart.write(data))
		self.echo = data
		while sel