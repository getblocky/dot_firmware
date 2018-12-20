#version=1.0

import sys
core = sys.modules['Blocky.Core']

class LED:
	def __init__(self,port):
		self.p = core.getPort(port)
		if self.p[0] == None : return 
		self.pin = core.machine.Pin(self.p[0],core.machine.Pin.OUT)
		self.pwm = core.machine.PWM(self.pin, duty = 0 , freq = 38000)
		self.pwm.deinit()
		
	def turn (self , value):
		try :
			if self.pwm :
				self.pwm.deinit()
			if isinstance(value,int):
				self.pin.value( value )
			else :
				if value == 'on':
					self.pin.value(1)
				elif value == 'off':
					self.pin.value(0)
				elif value == 'flip':
					self.pin.value(not self.pin.value())
		except :
			pass
				
	def fade(self , value):
		try :
			value = max(0,min(4095,value))
			self.pwm.init(duty = value , freq = 38000)
		except :
			pass