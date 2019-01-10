f._decode()
			bit_curr = 0
			self._clear()
			last_attempt = 0
			while True:
				h(None)
				
				if (self.length and self.prev_irq and d(u() , self.prev_irq) > 500000):
					print('__')
					last_attempt = u()
					self._correct()
					if self.length//2 != bit_length :
						print('differet length' , self.length//2 , bit_length)
						self._debug()
						self._clear()
						continue
					bit_curr = self._decode()
					if bit_curr == bit_prev :
						print('same' , bit_curr)
						self._clear()
						continue
						
					print('RECV {}'.format(self.length))
					print('Current bit mask = ' , bin(bit_mask))
					for x in range(bit_length):
						print('[C] {}      {} == {}'.format(x , self._bit(bit_curr,x),self._bit(bit_prev,x)),end='')
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
			
			
