(self,link):
		await self.gprs(True)
		await self.command('+HTTPTERM')
		await self.command('+HTTPINIT')
		await self.command('+HTTPPARA="URL","{}"'.format(link))
		await self.command('+HTTPPARA="CID",1')
		await self.command('+HTTPACTION=0')

		httpaction = await self.waitfor('+HTTPACTION')
		#self.cleanup = False
		httpread = await self.request('+HTTPREAD')
		print('BUFF', httpread)
		print(self.buffer)
		print('HTTP Received')
		print('Content = ' , httpread)
		#self.cleanup = True


	async def sendSMS(self,number,message):
		await self.command('+CMGF=1')
		await self.command('+CSCS="GSM"')
		await self.command('+CMGS="{}"'.format(number),response=[b'> '],iscmd=False)
		message = bytes(message,'utf-8') + bytes([0x1a])
		r = await self.request(message,prefix=b'+CMGS: ')
		print('SMS Sent, response = {}'.format(r))

	async def getSignalQuality(self):
		r = await self.request('+CSQ')
		return r[0]

	async def getOperator(self):
		r = await self.request('+COPS?')
		print('Operator retur