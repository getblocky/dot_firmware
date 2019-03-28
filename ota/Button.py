#version=3.0

import sys
core = sys.modules['Blocky.Core']

from machine import Pin


class Button:
	def __init__(self , port):
		self.p = core.getPort(port)
		self.port = port
		if self.p[0] == None :
			return
		self.ps = 0
		self.lt = {}
		self.his = []
		
		self.button = Pin(self.p[0] , Pin.IN , Pin.PULL_DOWN)
		self.button.irq(trigger = Pin.IRQ_RISING|Pin.IRQ_FALLING , handler = self._handler)
		core.deinit_list.append(self)
		core.mainthread.create_task(core.asyn.Cancellable(self._async_handler)())
	def event(self , type , time , function):
		function_name = str(type) + str(time)
		if not callable(function) :
			print('btn-event->Function cant be call')
			return
		self.lt[function_name] = function

	def is_pressed(self):
		return True if self.button.value() else False

	def _handler(self,source):
		s = self.button.value()
		if s == self.ps:
			return
		self.ps = s
		self.his.append(core.Timer.runtime())
		if len(self.his) < 2:
			return
		if self.his[-1] - self.his[-2]  > 500:
	