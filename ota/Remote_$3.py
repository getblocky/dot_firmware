ttempt and d(u() , last_attempt) > 3000000):
					break
			print('final bit mask = {}'.format(bin(bit_mask)))
			
			core._failsafeActive(True)
			self._recvActive(True)
			
			return
			if isinstance(name , str):
				self.learning = name
				print("[remote] Learning signal .. {} .. ".format(name))
		except Exception as err:
			import sys
			sys.print_exception(err)
	def _handler (self , source):
		if self.recv.value()!= self.last_state:
			self.last_state = not self.last_state
			self.time = ticks_us()
			if self.prev_irq == 0 :
				self.prev_irq = self.time
				return
			self.buffer[self.length] = ticks_diff(self.time,self.prev_irq)//50
			self.length += 1
			self.prev_irq = self.time
			
	
	def _correct(self):
		pos = 0
		while True :
			if (self.buffer[0] < self.buffer[1] and self.buffer[0] *2 < self.buffer[1]) or self.buffer[0] > 20000:
				print('correct')
				self.length -= 1
				for x in range(0 , self.length):
					self.buffer[x] = self.buffer[x+1]
			else :
				break
			
			
