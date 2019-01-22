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
			await self.command('+CDNSCFG="203.113.131.1"')


	async def http