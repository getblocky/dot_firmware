# SIM800 , AnataLAB

from machine import *
from time import *
import Blocky.uasyncio as asyncio
from _thread import *
mainthread = asyncio.get_event_loop()

class SIM800():
	def __init__(self):
		self.uart = UART(1,rx=25,tx=26,baudrate=9600)
		self.state = {}
		self._disableEcho()
		
	async def __routine__(self):
		
		

# Single Threaded !

await _getGSMLocation(self):
	test_at_responsive():
		send 'at'
		if receive 'ok' in timeout
			continue
		else 
			send again
			
	send_gsm_cmd():
		while self.running == True :
			sleep
		self.running = True
		
		get_result ( right after ) :
			send('gsm')
			se
		
		other :
			get_result ( waiting asyncio )
			this will :
				self.state['prefix'] = None
				send_cmd()
				while self.state['prefix'] == None :
					sleep 
					# the _routine will pick this up
				

All the message is parse with OK at the end
butttt
for some task , we must wait for some flag to be set 
for example 
	httpaction will trigger the http requests
	it will return ok 
	afte