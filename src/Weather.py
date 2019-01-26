#version=2.1
# AN2001
import sys
core = sys.modules['Blocky.Core']
from dht import *
from machine import Pin

class Weather:
	def __init__ (self , port,module='DHT11'):
		self.p = port
		self.pin = core.getPort(port)
		self.port = port
		if (self.p[0] == None):
			return
		if module == 'DHT11':
			self.weather = DHT11(Pin(self.pin[0]))
		else :
			raise NameError
		self.last_poll = core.Timer.runtime()
		#core.mainthread.create_task(self.handler())

	def temperature (self):
		if core.Timer.runtime() - self.last_poll > 2000:
			self.last_poll = core.Timer.runtime()
			try :
				self.weather.measure()
			except Exception:
				pass
		return self.weather.temperature()
	def humidity(self):
		if core.Timer.runtime() - self.last_poll > 2000:
			self.last_poll = core.Timer.runtime()
			try :
				self.weather.measure()
			except Exception:
				pass
		return self.weather.humidity()
		
	def deinit(self):
		Pin(self.p[0],Pin.IN)
