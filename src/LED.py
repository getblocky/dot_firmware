#version=2.0

import sys
core = sys.modules['Blocky.Core']

class LED:
	def __init__(self,port):
		self.p = core.getPort(port)
		if self.p[0] == None : return 
		self.pwm = core.machine.PWM(self.pin, duty = 0 , freq = 38000)
		
	def turn (self , value):
		try :
			if isinstance(value,int):
				if value == 0 :
					self.pwm.duty(0)
				elif value == 1 :
					self.pwm.duty(1023)
			else :
				if value == 'on':
					self.pwm.duty(1023)
				elif value == 'off':
					self.pwm.duty(0)
				elif value == 'flip':
					if self.pwm.duty() == 0 :
						self.pwm.duty(1023)
					else self.pwm.duty(0)
		except :
			pass
				
	def fade(self , value):
		try :
			value = max(0,min(1023,value))
			self.pwm.init(duty = value , freq = 38000)
		except :
			pass