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
		pr