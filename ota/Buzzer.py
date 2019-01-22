#version=2.0

import sys;core=sys.modules['Blocky.Core']
from machine import Pin,PWM
class Buzzer:
	def __init__(self,port):
		self.port = port
		self.p = core.getPort(port)
		self.pwm = PWM(Pin(self.p[0]),duty = 0,freq=38000)
		core.deinit_list.append(self)
	def turn(self,value):
		try:
			if isinstance(value,int):
				if value == 1:
					self.pwm.freq(38000)
					self.pwm.duty(1023)
				if value == 0:
					self.pwm.duty(0)
			elif isinstance(value,str):
				if value == 'on':
					self.pwm.freq(38000)
					self.pwm.duty(1023)
				if value == 'off':
					self.pwm.duty(0)
				if value == 'flip':
					if self.pwm.duty() == 0:
						self.turn(1)
					else :
						self.turn(0)
		except :
			pass

	async def beep(self,time=1,speed=200):
		self.turn(0)
		for x in range(0,time*2):
			self.turn('flip')
			await core.wait(speed)
		self.turn(0)

	async def play(self,sequence,gap=10,duty=None):
		try :
			if isinstance(sequence,int):
				self.pwm.freq(sequence)
				self.pwm.duty(duty or 100)
			i