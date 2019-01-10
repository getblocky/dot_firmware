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
	after finish , it return a +httpaction flag
	the function that require this must wait for this flag to be set
	this flag will be set by the rountine , therefore , there are offtime
	
	for others task like http read
	sim800 return the string immediately , what if inside the content we have "OK" :)
	example 
		>>> AT+HTTPREAD
		<<< +HTTPREAD :8
		<<< hello OK
		<<< OK
	with this one , the routine must be a bit smarter to realize that 8 bytes is data !
	
	
	
	
In Conjunction with common funciton :
	there are 2 kind of operation 
		AaA ( ask and answer ):
			this operation will set the flag preventi
			
		Event -> __routine__
			exitCondition = any() = 1 and buf.endswith('OK\r\n')
			
	
	
	
	
	
	
	
	
	
	
	