f.uart.any() == 0:
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
		await self.command('+CIICR')
		await self.request('+CIFSR')
		#await self.command('+CMEE=2')
		#await self.command('+CIFSR;E0',prefix = '11.185.172.8')
		await self.command('+CDNSCFG="203.113.131.1"')
		
		#await self.command('+CIPSSL=1')
		# modemConnect
		#r = await self.command('+CIPSTART=1,"TCP","blynk.getblocky.com",9443',prefix = ["1, CONNECT OK","CONNECT FAIL","ALREADY CONNECT","ERROR","CLOSE OK"])
		r = await self.command('+CIPSTART=2,"TCP","blynk.getblocky.com",80',prefix = ["2, CONNECT OK","CONNECT FAIL","ALREADY CONNECT","ERROR","CLOSE OK"])
		if r == 0 :
			print('[Blynk] Connect successfully !')
ext_socket = SIM800()


#version=2.0

# The MIT License (MIT)
# Copyright (c) 2015-2018 Volodymyr Shymanskyy
# Copyright (c) 2015 Daniel Campora

"""
	Add support for external socket hook 
		+ SIM800L GPRS Networking
		+ A9G
		+ SIM808
"""

from micropython import const
HDR_LEN = const(5)
HDR_FMT = "!BH