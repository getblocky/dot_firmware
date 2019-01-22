from machine import UART,Pin
from time import *
from _thread import start_new_thread
import Blocky.uasyncio as asyncio
mainthread = asyncio.get_event_loop()
import gc,re,sys,os
from neopixel import NeoPixel
REQUEST = 1
COMMAND = 2
EVENT   = 3
PARSE   = 4

n = NeoPixel(Pin(5),12,timing=True)
def state(num,s):
	n.fill((0,0,0))
	n[num] = (5,5,5) if s == 1 else  (0,0,0)
	n.write()

sleep_ms(2000)

class SIM800:
	def __init__(self):
		self.uart = UART(1,rx=25,tx=26,baudrate=9600)
		self.buffer = b''
		self.echo = b''
		self.running = False
		self.polling = False

		self._liEvent = {}
		self._liRequest = None
		self._liCommand = None
		self.belonged = False
		self._string = b''
		self._liSocket = [None for _ in range(6)]

		self.gprs_connected = False
		mainthread.create_task(self.routine())
		mainthread.create_task(self.gprs(True))


	def __repr__(self):
		if self.buffer != None :
			print('[buffer]' , self.buffer)
		if self._liCommand != None :
			print('[command]' , self._liCommand)
		if 