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
						core.indicator.rgb.fill((10,0,0));core.indicator.rgb.write()
						sleep_ms(10)
						core.indicator.rgb.fill((0,0,0));core.indicator.rgb.write()
						print('differet length' , self.length//2 , bit_length)
						self._debug()
						self._clear()
						continue
					bit_curr = self._decode()
					if bit_curr == bit_prev :
						core.indicator.rgb.fill((0,10,0));core.indicator.rgb.write()
						sleep_ms(10)
						core.indicator.rgb.fill((0,0,0));core.indicator.rgb.write()
						print('same' , bit_curr)
						self._clear()
						continue

					print('RECV {}'.format(self.length))
					print('Current bit mask = ' , bin(bit_mask))
					for x in range(bit_length):
						print('[C] {}      {} == {}'.format(x , self._bit(bit_curr,x),se