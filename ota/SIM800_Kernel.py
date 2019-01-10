from machine import UART
from time import *
from _thread import *
import Blocky.uasyncio as asyncio
mainthread = asyncio.get_event_loop()
import gc , sys , os , re

"""
	This library implement SIM800 core functionality that is relevant to Blocky Platform
	Since this module is not very responsive , the libray is mostly written in asyncio
	Feature :
		+ create seperated socket (0-5) , each socket will have
			+ getaddrinfo(host,port) , this is a dummy one for compatibility reason
			+ connect(host,port) or (getaddrinfo[0][-1])
			+ send(buffer)
			+ recv(length)
			+ settimeout(time)
			+ setsockopt(mode,callback)
			+ close()
			+ sendto()
			
		+ gsm :
			+ send , receive message
			+ read saved SMS , draft ... have no use -> NotImplementedError
			+ calling , hangup is not written
			+ getOperator()
			+ getSignalQuality()
			+ getGSMLocation()
			+ getSIMIMEE()
			+ unlockSIM(pin)
			
			
		+ TCP Server is not implemented . and will not be due to its limitation
		
			

"""

class lStr :
	def __init__(self):
		self.buf = b''
		
	def __add__ (self,other):
		pass
	def __getitem__(self,key):
		pass
	def __delitem__(self,key):
		pass
	def __setitem__(self,key):
		pass
	def __contains__(self,item):
		pass
	def __missing__(self,key):
		pass
	def __iter__ (self):
		pass
	def __next__(self):
		pass
	def __len__(self):
		pass

class SIM800 :
	def __init__(self):
		self.uart = UART(1,rx = 25,tx=26,baudrate=9600)
		self.debugport = UART(2,tx=32,rx=33,baudrate=9600)
		self.buffer = b''
		self.echo = b''
		self._liEvent = {}
		
		self.running = False
		
		self._liEvent = {}
		self._liRequest = None
		self._liCommand = None
		self.polling = False
		self.cleanup = True
		self.belonged = False
		
		self._liSocket = [None for _ in range(6)]
		
		mainthread.create_task(self.routine())
		
	def socket(self,*args,**kwargs):
		class socket :
			def __init__(self,super,mode = 0):
				self.super = super
				self.id = self.super._liSocket.index(None)
				self.super._liSocket[self.id] = sel