lf._bit(bit_prev,x)),end='')
						if self._bit(bit_curr,x) != self._bit(bit_prev,x):
							bit_mask = self._bit(bit_mask,x,0)
							print('###')
						else :
							print()
					print('BIT_MASK ' , bin(bit_mask))

					bit_prev = bit_curr
					self._clear()

				if (last_attempt and d(u() , last_attempt) > 3000000):
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
			self.buffer[self.length] = min(255,ticks_diff(self.time,self.prev_irq)//50)
			self.length += 1
			self.prev_irq = self.time


	def _correct(self):
		