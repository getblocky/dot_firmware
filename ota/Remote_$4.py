			
	@core.asyn.cancellable
	async def _routine (self):
		while True :
			await core.wait(1000)
			if self.length > 0 and core.time.ticks_diff(core.time.ticks_us() , self.prev_irq) > 1000000:
				self._recvActive(False)
				self._correct()
				self.bin = self._decode(self.buffer , self.length)
				if self.learning :
					self._store (self.learning , self.buffer , self.bin , self.length)
					print("[remote] Signal ..{}.. is learnt".format(self.learning))
					self.learning = None
				else :
					name = self._recognise(self.bin)
					if name :
						core.mainthread.call_soon(core.call_once("user_remote_{}_{}".format(self.port, name),self.event_list[name][1]))
				
				self._debug()
				sleep_ms(1000)
				self.send(self.buffer , self.length)
				self.length = 0
				self.prev_irq = 0
				for x in range(len(self.buffer)):
					self.buffer[x] = 0
				self._recvActive(True)
			
	
	def _debug(self):
		print("__________________RECV	{}	______ {} _______".format(self.length , self.bin))
		for x 