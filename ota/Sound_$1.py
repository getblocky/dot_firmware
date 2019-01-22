me)]))
					await core.call_once('user_sound_{}_{}'.format(self.port , self.time),self.func[str(self.time)])
				except Exception as err:
					print('[sound->exec] -> {}'.format(err))
				finally :
					self.time = 0

	def _handler(self , source):
		if core.Timer.runtime() - self.last > 100 :
			self.last = core.Timer.runtime()
			self.time += 1

	def getSoundLevel (self):
		return self.adc.read()

	def deinit(self):
		self.pin.irq(trigger=0)
		Pin(self.p[0],Pin.IN)
