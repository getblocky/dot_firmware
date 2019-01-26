from machine import UART
from time import *
from _thread import *
import Blocky.uasyncio as asyncio
mainthread = asyncio.get_event_loop()

import gc,sys

class SIM800:
	def __init__(self):
		self.uart = UART(1,rx=25,tx=26,baudrate=9600)
		self.buf =  b''
		self.running = False
		self.echo = b''
		self.dict = {} # this is where change saved
		self.responselist = [] # ['OK','ERROR']
		self.waitinglist = [b'+CPIN',b'Call Ready',b'SMS Ready',b'RDY']	# ['SMS Ready','Call Ready']
		self.data = b''
		self.sendtime = ticks_ms()
		
		mainthread.create_task(self.routine())
		
	def write(self,cmd):
		if isinstance(cmd,str):
			buf = b'AT' + bytes(cmd,'utf-8') + b'\r\n'
			self.echo = b'AT' + bytes(cmd,'utf-8') + b'\r\r\n' #TODO
		elif isinstance(cmd,bytes):
			buf = b'AT' + cmd + b'\r\n'
			self.echo = b'AT' + cmd + b'\r\r\n'
		else :
			raise Exception
			return
		print('\t\t[WRITE]' , buf)
		self.uart.write(buf)
		self.sendtime = ticks_ms()
		
	async def waitReady(self,timeout = 1000):
		while self.running == True:
			await asyncio.sleep_ms(1)
		self.running = True
		
		self.responselist = [b'OK']
		self.write('')
		#print('\t',end='')
		while True :
			print('#',end='')
			await asyncio.sleep_ms(50)
			
			for _ in range(10):
				if isinstance(self.responselist,list) and b'OK' in self.responselist:
					await asyncio.sleep_ms(10)
				else :
					break
			if isinstance(self.responselist,list) and b'OK' in self.responselist:
				self.write('')
			else :
				#print('\t<ready>')
				break
				
		
			
				
		
		
	async def command(self,cmd,prefix=['OK','ERROR'],timeout=1000):
		print('\t[SIM800] Command' , cmd , end = '')
		# Make sure the module is ready
		await self.waitReady(timeout)
		self.responselist = []
		for x in range(len(prefix)):
			self.responselist.append(bytes(prefix[x],'utf-8') if isinstance(prefix[x],str) else prefix[x])
		
		self.write(cmd)
		while isinstance(self.responselist,list):
			await asyncio.sleep_ms(1)
		
		
		r = self.responselist
		self.running = False
		print(r)
		return r
		
		
	async def request(self,cmd,prefix = None,timeout = 1000):
		# Make sure the module is ready
		
		print('\t[SIM800] Request',cmd,end='')
		if prefix == None :
			prefix = ''
			for x in range(len(cmd)):
				if cmd[x].isalpha() or cmd[x] == '+':
					prefix += cmd[x]
				else :
					break
			prefix = bytes(prefix,'utf-8')
		else :
			if isinstance(prefix,str):
				prefix = bytes(prefix,'utf-8')
			
		cmd= bytes(cmd,'utf-8') if isinstance(cmd,str) else cmd
		await self.waitReady(timeout)
		#print('Requesting [{}] [{}]'.format(cmd,prefix))
		self.write(cmd)
		if not prefix in self.waitinglist:
			self.waitinglist.append(prefix)
		while prefix in self.waitinglist:
			await asyncio.sleep_ms(1)
			#print('>',end='')
		#print('\t <<< Return [{}]'.format(self.dict[prefix]))
		self.running = False
		print("\t[SIM800] Request Done -> ",self.dict[prefix])
		return self.dict.pop(prefix)
		
	async def getSignalQuality(self):
		r = await self.request('+CSQ')
		return r
			
		
	async def routine(self):
		# In harmonic with command and request
		self.buf = b''
		while True :
			await asyncio.sleep_ms(5)
			if self.uart.any() == 0 and len(self.buf) > 0:
				print('\t\t\t<buf>',self.buf)
				if self.buf.startswith(self.echo):
					self.buf = self.buf[len(self.echo):]
				while self.buf.startswith(b'\r\n'):
					self.buf = self.buf[2:]
				resp = self.buf[0:self.buf.find(b'\r\n')]
				data = self.buf[self.buf.find(b'\r\n')+2:self.buf.rfind(b'\r\n\r\nOK\r')]
				# resp contains cmd and ans , see +HTTPREAD
				if resp.count(b': '):
					cmd,ans = resp.split(b': ')
				else :
					cmd = resp
					ans = b''
				ans = ans.split(b',') if ans.count(b',') else [ans]
				for x in range(len(ans)):
					try :
						ans[x] = int(ans[x]) if ans[x].count(b'.') == 0 else float(ans[x])
					except :
						pass
					
				print('\t[SIM800] Receive ',cmd,ans,data,self.buf)
				#print('<raw>',cmd,ans,resp,data)
				if isinstance(self.responselist,list) and cmd in self.responselist:
					self.responselist = self.responselist.index(cmd)
					#print('<recv> Reponse = {}'.format(self.responselist))
				elif cmd in self.waitinglist:
					if cmd in self.waitinglist : # Damn you CIFSR
						self.waitinglist.remove(cmd)
						self.dict[cmd] = ans
						if len(data):
							data = data[0:-5]
							self.dict[cmd].append(data)
					else :
						print('No prefix' , self.echo, cmd)
				else :
					prefix = self.echo[2:-3]
					if prefix in self.waitinglist:
						self.waitinglist.remove(prefix)
					self.dict[prefix] = cmd
					#print('<recv> Request = {}'.format(self.dict[cmd]))
				self.buf = b''
				
			if self.uart.any() > 0:
				self.buf = self.uart.read()
	async def sendSMS(self,number,message):
		#print('Sending SMS to ', number)
		await self.command('+CMGF=1')
		await self.command('+CSCS="GSM"')
		await self.command('+CMGS="{}"'.format(number),prefix=['>'])
		#print('Message = ',message)
		self.uart.write(message)
		self.uart.write(bytearray([0x1A]))
		#print('Done')
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
		await self.command('+CIICR')
		await self.request('+CIFSR')
		#await self.command('+CMEE=2')
		#await self.command('+CIFSR;E0',prefix = '11.185.172.8')
		await self.command('+CDNSCFG="203.113.131.1"')
		
		#await self.command('+CIPSSL=1')
		# modemConnect
		#r = await self.command('+CIPSTART=1,"TCP","blynk.getblocky.com",9443',prefix = ["1, CONNECT OK","CONNECT FAIL","ALREADY CONNECT","ERROR","CLOSE OK"])
		r = await self.command('+CIPSTART=1,"UDP","blynk.getblocky.com",80',prefix = ["1, CONNECT OK","CONNECT FAIL","ALREADY CONNECT","ERROR","CLOSE OK"])
		if r == 0 :
			print('[Blynk] Connect successfully !')
ext_socket = SIM800()
sim = ext_socket




mainthread.create_task(main())
mainthread.run_forever()
start_new_thread(mainthread.run_forever,())
		
		
		
			