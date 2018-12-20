#version=1.0
import sys
core=sys.modules['Blocky.Core']
class Relay :
	def __init__(self , port):
		self.p = core.getPort(port)
		if self.p[0] == None :
			return 
		self.switch = Pin(self.p[0] , Pin.OUT)
		self.switch.value(0)
		
	def turn(self , state):
		try :
			if isinstance(state , int):
				self.switch.value(state)
			elif isinstance(state , str):
				if state == 'on':
					self.switch.value(1)
				elif state == 'off':
					self.switch.value(0)
				elif state == 'flip':
					self.switch.value(not self.switch.value())
		except :
			pass
	def state(self)::
		return self.switch.value()
	def flip(self):
		self.switch.value(not self.switch.value())

