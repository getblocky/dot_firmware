#version=2.0
import sys
core = sys.modules['Blocky.Core']
from machine import Pin
class Motion :
	def __init__(self , port):
		self.p = core.getPort(port)
		self.port = port
		if self.p == None :
			return
		self.motion = Pin(self.p[0],Pin.IN,Pin.PULL_DOWN)
		self.whendetect = None
		self.whennotdetect = None
		self.prev = self.motion.value()
		core.mainthread.create_task(core.asyn.Cancellable(self._handler)())
		core.deinit_list.append(self)

	@core.asyn.cancellable
	async def _handler(self):
		while True :
			if self.motion.value() != self.prev :
				if self.motion.value():
					if self.whendetect :
						await core.call_once('user_motion_{}_{}'.format(self.port , 1) , self.whendetect)
				else:
					if self.whennotdetect :
						await core.call_once('user_motion_{}_{}'.format(self.port , 0) , self.whennotdetect)
				self.prev = not self.prev

			await core.wait(300)  #Update rate

	def event(self,type,function):
		if callable(function):
			if type == 'detect' :
				self.whendetect = function
			else :
				self.whennotdetect = function
	def deinit(self):
		Pin(self.p[0] , Pin.IN)
