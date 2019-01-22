#version=2.0

import sys
core = sys.modules['Blocky.Core']
from machine import ADC , Pin , PWM
class WaterSensor :
	def __init__ (self , port , range = 3.3):
		self.p = core.getPort(port)
		if (self.p[2] == None):
			return
		self.port = port
		self.adc = ADC(Pin(self.p[2],Pin.IN))
		PWM(Pin(self.p[0],Pin.IN)).deinit()
		Pin(self.p[0] , Pin.IN)
		self.supply = Pin(self.p[1],Pin.OUT)

		if (range == 1.1):		self.adc.atten(ADC.ATTN_0DB)
		elif (range == 1.5):	self.adc.atten(ADC.ATTN_2_5DB)
		elif (range == 2.2):	self.adc.atten(ADC.ATTN_6DB)
		elif (range == 3.3):	self.adc.atten(ADC.ATTN_11DB)
		core.deinit_list.append(self)

	def value(self):
		self.supply.value(1)
		val = self.adc.read()
		self.supply.value(0)
		return abs(4095-val)

	def deinit(self):
		Pin(self.p[1],Pin.IN)
