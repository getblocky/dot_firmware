03.113.131.1"')
			
	
	async def http(self,link):
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
		
	async def sync_ntp (self):
		await self.command('+CIPSTART=1,"UDP","pool.ntp.org",123', response =[b'1, CONNECT OK'])
		a = bytearray(48)
		a[0] = 0x1b
		a = bytes(a)
		await self.command('+CIPSEND=1,48' , response= [b'> '])
		r = await self.request(a,prefix = b'DATA ACCEPT:1,')
		print('DATA ACCEPTED >>>>>>>. ' , r)
		buf =  b''
		await self.waitfor('+CIPRXGET: 1,1')
		a = await self.request('+CIPRXGET=4,1',prefix= b'+CIPRXGET: 4,1,')
		a = await self.request('+CIPRXGET=2,1,{}'.format(a[0]),prefix = b'**')
		print("NTP_BUFFER" , a)
		await self.command('+CIPCLOSE=1,0',response = [b'1, CLOSE OK'])
		import struct
		val = struct.unpack("!I", a[0][40:44])[0] - 3155673600
		
		import time,machine
		tm = time.localtime(val)
		tm = tm[0:3] + (0,) + tm[3:6] + (0,)
		machine.RTC().datetime(tm)
		print("CURRENT TIME IS " , time.localtime())
		
	async def sendSMS(self,number,message):
		await self.command('+CMGF=1')
		await self.command('+CSCS="GSM"')
		await self.command('+CMGS="{}"'.format(number),response=[b'> '])
		message = bytes(message,'utf-8') + bytes([0x1a])
		r = await self.request(message,prefix=b'+CMGS: ')
		print('SMS Sent, response = {}'.format(r))
		
	async def getSignalQuality(self):
		r = await self.request('+CSQ')
		return r[0]
		
	async def getOperator(self):
		r = await self.request('+COPS?')
		if len(r) > 1:
			return [r[1],r[2]]
		else :
		print('Operator return {}'.format(None if len(r) <= 1 else [r[1],r[2]]))
		return None if le