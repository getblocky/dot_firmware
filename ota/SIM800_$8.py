type)
		return _socket_
	async def sendSMS(self,number,content):
		await self.c('+CMGF=1')
		await self.c('+CSCS="GSM"')
		await self.c('+CMGS="{}"'.format(number),r=[b'> '])
		m=bytes(content,'utf-8')+b'\x1a'
		self.u.write(m)
	async def rSMS(self):
		while True:
			try:
				await s(100)
			except OSError:
				pass
				#a = \'\xc1 H\xed H\xed\'

	async def readSMS(self,i):
		r = await self.r('+CMGR={}'.format(i),w='+CMGR: ')
		return r
	def whenReceiveSMS(self,function):
		self._fsms = function
	def deinit(self):
		core.eeprom.set('EXT_SOCKET',False);core.hardware['uart'][self.i]=N
