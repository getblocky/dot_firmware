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
		self.running = Fa