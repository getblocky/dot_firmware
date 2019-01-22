#version=2.0

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
			print('hold for ' , (self.his[-1] - self.his[-2] )// 1000 ,'seconds')
			self.execute('hold' ,  (self.his[-1] - self.his[-2] )// 1000 )
			self.his.clear()
	@core.asyn.cancellable
	async def _async_handler (self):
		while True :
			await core.wait(500)
			if self.button.value() == 0:
				if len(self.his) and (core.Timer.runtime() - self.his[-1]) > 500 :
					print('pressed ' , len(self.his)//2)
					core.mainthread.call_soon(self.execute('pressed' ,len(self.his)//2 ))
					self.his.clear()

	async def execute(self,type,time):
		try :
			function = self.lt.get( str(type) + str(time) )
			if function == None :
				raise Exception

			if core.flag.duplicate == False :
				await core.call_once('user_button_{}_{}_{}'.format(self.port,type,time) , function)
			else:
				core.mainthread.create_task(core.asyn.Cancellable(function)())

		except Exception as err:
			print('btn-exec->' , err)
			pass

	def deinit(self):
		self.button.irq(trigger=0)
		Pin(self.p[0],Pin.IN)
