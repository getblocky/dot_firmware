from machine import UART,Pin
from time import *
from _thread import *
import Blocky.uasyncio as asyncio
mainthread = asyncio.get_event_loop()
import gc , sys , os , re
from neopixel import NeoPixel
n = NeoPixel(Pin(5),1, timing = True)

p = Pin(12 ,Pin.PULL_UP)
if p.value() == 0:
  import os
  os.remove('main.py')
  import machine
  machine.reset()

class SIM800 :
	def __init__(self,debug = True):
		self.uart = UART(1,rx = 25,tx=26,baudrate=9600)
		self.debugport = UART(2,tx=32,rx=33,baudrate=9600)
		self.buffer = b''
		self.echo = b''
		self._liEvent = {}
		self.debug = debug
		self.running = False

		self._liEvent = {}
		self._liRequest = None
		self._liCommand = None
		self.polling = False
		self.cleanup = True
		self.belonged = False

		self._liSocket = [None for _ in range(6)]

		mainthread.create_task(self.routine())
	def getaddrinfo(self,host,port):
		return [[None,None,None,None,(host,port)]]

	def socket(self,*args,**kwargs):
		class socket :
			def __init__(self,super,mode = 0):
				self.super = super
				self.id = self.super._liSocket.index(None)
				self.super._liSocket[self.id] = self


				self.sockMode= mode # 2 if UDP , 0 if TCP



			async def close(self):
				r = await self.super.command('+CIPCLOSE={},0'.format(self.id),\
					response = [bytes(str(self.id),'utf-8') + b', ' + \
					x for x in [b'CLOSE OK',b'ERROR']]\
				);return r==0

			async def connect(self,addr):
				#await self.super.command('+CSTT="v-internet"')
				#await self.super.command('+CIICR')
				#await self.super.command('+CIFST',response = [b'*'])
				r = await self.super.command(\
					'+CIPSTART={id},"{mode}","{addr}",{port}'.format(\
						id = self.id,\
						mode = "UDP" if self.sockMode == 2 else "TCP",\
						addr = addr[0],\
						port = addr[1]), \
					response = [bytes(str(self.id),'utf-8') + b', ' + x for x in [b'CONNECT OK',b'ALREADY CONNECT',b'CONNECT FAIL'] ]\
				);return False if r == 2 else True
			async def recv(self,length):
				await self.super.waitfor('+CIPRXGET: 1,{id}'.format(id=self.id))
				r = await self.super.request('+CIPRXGET=2,{id},{length}'.format(id=self.id,length=length),	prefix = b'**')
				# r = [RECEIVED,PENDING]
				if r[0] == length:
					return #TODO ERROR HERE
				return r

			async def listen(self):
				pass

			async def read(self):
				pass

			async def readinto(self):
				pass

			async def readline(self):
				pass


			async def recvfrom(self):
				pass

			async def send(self):
				pass

			async def sendall(self):
				pass


			async def setblocking(self):
				pass

			async def setsockopt(self):
				pass
			async def sendto(self,data,addr):
				await self.connect( addr)
				await self.write( data )

			async def write(self , data , length = None):
				r = await self.super.command('+CIPSEND={id},{length}'.format(id = self.id , length = len(data) if length == None else data[:length]),\
					response = [b'> '])
				if not isinstance(data,bytes):
					try :
						if isinstance(data,str):
							data = bytes(data,'utf-8')
						elif isinstance(data,bytearray):
							data = bytes(data)
					except TypeError as error:
						import sys
						sys.print_exception(error)
						if self.debug :
							print('[ERROR] Can not convert to bytes')
							print('BUF = ',data)

				r = await self.super.request(data , prefix = b'DATA ACCEPT:{},'.format(self.id),iscmd=True)

		new_socket = socket(self , *args,**kwargs)
		return new_socket

	def trigger (self,kw,func):
		pass




	async def waitReady(self):
		return
		while self.running == True :
			await asyncio.sleep_ms(1)
		self.running = True
		self.polling = True
		while True :
			if len(self.buffer):
				self.parsing()
			await self.write(b'AT\r\n')
			await asyncio.sleep_ms(100)
			if self.uart.any() > 0:
				temp=self.uart.read();self.buffer+=temp;self.debugport.write(b'>>>'+temp)
				if self.debug :
					print('\t\t[READY]\t\t' , end = '')
				if b'OK' in self.buffer:
					self.polling = False
					self.running = False
					return
				self.parsing()



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
		print('Operator return {}'.format(None if len(r) <= 1 else [r[1],r[2]]))
		return None if len(r) <= 1 else [r[1],r[2]]



# =================== Test Case ======================
a = SIM800()
b = a.socket(2)
async def app():
	await a.gprs(True)
	while True :
		ntp = bytearray(48)
		ntp[0] = 0x1b
		addr = a.getaddrinfo("pool.ntp.org",123)[0][-1]
		res = await b.sendto(ntp,addr)
		msg = await b.recv(48)
		b.close()
		print('MSG = ' , msg)

async def app2():
	while True :
		r = await a.request('+CADC?')
		print('ADC', r)
		await asyncio.sleep_ms(10000)



mainthread.create_task(app())
mainthread.create_task(app2())
start_new_thread(mainthread.run_forever,())
