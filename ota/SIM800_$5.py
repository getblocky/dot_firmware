min(len(d),self.lr)]
			if len(self.lr) < length:
				missing=length - len(self.lr);self.lr +=self.b[0:missing];self.b=self.b[missing:]
	async def connect (self):
		self.u.write('ATE0\r\n');self.u.read();r=await self.r('+CFUN?')
		if r[0] !=1:
			r=await self.c('+CFUN=1')
			if r !=0:
				return F
		r=await self.r('+CGATT?')
		if r[0] !=1:
			while True:
				r=await self.c('+CGATT=1')
				if r==0:
					break
		await self.c('+SAPBR=3,1,"Contype","GPRS"');await self.c('+SAPBR=3,1,"APN","{}"'.format(self.s['apn']));await self.c('+SAPBR=3,1,"USER","{}"'.format(self.s['user']));await self.c('+SAPBR=3,1,"PWD","{}"'.format(self.s['pwd']));await self.c('+CGDCONT=1,"IP","{}"'.format(self.s['apn']));await self.c('+CGACT=1,1',to=10000);await self.c('+SAPBR=1,1',to=5000);await self.r('+SAPBR=2,1',w=b'+SAPBR:',to=5000);await self.c('+CGATT=1');await self.c('+CIPMUX=1');await self.c('+CIPQSEND=1');await self.c('+CIPRXGET=1');await self.c('+CSTT="{}"'.format(self.s['apn']));await self.c('+CIICR');awa