#version=2.0

import sys;core=sys.modules['Blocky.Core']

class Buzzer:
	def __init__(self,port):
		self.port = port
		self.p = core.getPort(port)
		self.pwm = core.machine.PWM(core.machine.Pin(self.p[0]),duty = 0,freq=38000)
	
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
			if isinstance(sequence,list):
				if len(sequence) % 2 == 0:
					self.pwm.duty(duty or 100)
					for x in range(0,len(sequence),2):
						if sequence[x] != 0 :
							self.pwm.freq(sequence[x])
						else :
							self.pwm.duty(0)
						await core.wait(sequence[x+1])
						self.pwm.duty(0)
						await core.wait(gap)
						self.pwm.duty(duty or 100)
					self.pwm.duty(0)
		except (TypeError,ValueError) as err :
			import sys
			sys.print_exception(err)
			pass
			
			
