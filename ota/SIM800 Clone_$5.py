nt('Done')
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
