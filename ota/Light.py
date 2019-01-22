#version=2.0
import sys
core = sys.modules['Blocky.Core']
from machine import Pin , PWM , ADC
class Light :
	def __init__ (self , port , range = 3.3):
		self.pin = core.getPort(port)
		if (self.pin[2] == None):
			return
		self.port = port
		PWM(Pin(self.pin[0],Pin.IN)).deinit()
		Pin(self.pin[0] , Pin.IN)

		self.adc = ADC(Pin(self.pin[2],Pin.IN))

		if (range == 1.1):		self.adc.atten(ADC.ATTN_0DB)
		elif (range == 1.5):	self.adc.atten(ADC.ATTN_2_5DB)
		elif (range == 2.2):	self.adc.atten(ADC.ATTN_6DB)
		elif (range == 3.3):	self.adc.atten(ADC.ATTN_11DB)
		core.deinit_list.append(self)

	def value(self):
		return self.adc.read()

	def deinit(self):
		pass
