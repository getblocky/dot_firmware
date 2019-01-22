int('Done')
		
		
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