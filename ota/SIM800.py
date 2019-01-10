from machine import UART
from time import *
from _thread import *
import Blocky.uasyncio as asyncio
mainthread = asyncio.get_event_loop()

import gc,sys
# Routine classes
	# _jEvent , _jCommand , _jRequest , _jPolling
	"""
		_jEvent :
			-> Handle task data that come from SIM800 without being asked.
			=> Typical use is +CIPRXGET: 1,1 (SIM800 notify that socket 1 received a msg)
			For this kind , the keyword is the whole "+CIPRXGET: 1,1"
			Save it to self._lEvent
		_jCommand :
			-> Handle command , you send a command , you provide what the module might answer
			as a list , this function return the index of that answer in the list
		_jRequest :
			-> Requesting  a data field . Get the data.
		_jPolling :
			Definging 
			
		_jCommand and _jRequest is a closed. The module will reply right away and only one of each is allow to be active
		But , _jEvent can occur at any time , therefore it might get into the buffer that these two function are handling
		Therefore , the method is to check if any event string is inside 
		buf = 'joijwoijfjojwiefOKijweogiweG+CIPRXGET:1,1\n\n\aofijqoijg'
		
	"""
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
		self.writer = asyncio.StreamWriter(self.uart,{})
		self.reader = asyncio.StreamReader(self.uart)
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
	
	