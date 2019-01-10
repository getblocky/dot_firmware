		print('[SIM800] Perform Receiving')
		buf = b''
		availalbe  = 0
		await self.request('+CIPRXGET=2,1,{}'.format(size))
		for x in range(10) :
			a = await self.request('+CIPRXGET=4,1')
			await asyncio.sleep_ms(500)
			if not (a[0] == 4 and a[1] == 1) :
				continue
			if a == [4,1,5] :
				print('#'*50)
				print('#'*50)
				print('#'*50)
				print()
			if a[2] > 0 :
				print('@'*50)
				print('@'*50)
				print('@'*50)
				availalbe += a[2]
				temp =  await self.request('+CIPRXGET=2,1,{}'.format(a[2]))
				print('[SIM800] Data Packages Receive = ' , temp[4],end = '')
				buf = temp[4]
				print("Received" , availalbe,'/',size)
				
		return buf
		
	async def send(self,data):
		print('[SIM800] Sending' , data)
		await self.command('+CIPSEND=1,{}'.format(len(data)),prefix=['>'])
		print('[SIM800] Sending Package = ' , data,end='')
		print('Sent' , self.uart.write(data))
		self.echo = data
		while self.uart.any() == 0:
			pass
		temp = self.uart.read()
		print('DATA_RES' , temp)
		print('Done')
		
		
	async def close(self):
		print('[SIM800] Closing')
	async def connect(self,server,port):
		print('[SIM800] Connecting',server,port)
		while True :
			r = await self.getSignalQuality()
			if r[0] == 0 :
				await asyncio.sleep_ms(100)
			else :
				break
		
		await self.command('+CIPSHUT',prefix = ['SHUT OK'])
		await self.command('+CGATT=0')
		await asyncio.sleep_ms(1000)
		await self.command('+CGATT=1')
		await self.command('+CFUN=1')
		await self.command('+SAPBR=3,1,"Contype","GPRS"')
		await self.command('+SAPBR=3,1,"APN","v-internet"')
		await self.command('+SAPBR=3,1,"USER",""')
		await self.command('+SAPBR=3,1,"PWD",""')
		await self.command('+CGDCONT=1,"IP","v-internet"')
		await self.command('+CGACT=1,1')
		await self.command('+SAPBR=1,1')
		await self.request('+SAPBR=2,1')
		await self.command('+CGATT=1')
		await self.command('+CIPMUX=1')
		await self.command('+CIPQSEND=1')
		await self.command('+CIPRXGET=1')
		await self.command('+CSTT="v-internet"')
		awai