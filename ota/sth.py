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
			def __init__(self,super,mode = 