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
				if (last_a