#version=2.0

import sys
core = sys.modules['Blocky.Core']
from machine import Pin
class Sound :
	def __init__ (self , port):
		self.p = core.getPort(port)
		self.port = port
		if self.p[1] == None or self.p[2] == None :
			return

		self.pin = Pin(self.p[1],Pin.IN,Pin.PULL_UP)
		self.adc = core.machine.ADC(Pin(self.p[2]))
		self.adc.atten(core.machine.ADC.ATTN_11DB)

		self.last = core.Timer.runtime()
		self.time = 0
		self.func = {}

		self.pin.irq(trigger = Pin.IRQ_FALLING , handler = self._handler)
		core.mainthread.create_task(core.asyn.Cancellable(self._async_handler)())
		core.deinit_list.append(self)

	def event (self , time , function):
		function_name = str(time)
		if not callable(function):
			return
		self.func[function_name] = function

	@core.asyn.cancellable
	async def _async_handler(self):
		while True :
			await core.wait(500)
			if core.Timer.runtime() - self.last > 500 and self.time > 0 :
				try :
					print('[sound] -> {}->{}'.format(self.time,self.func[str(self.ti