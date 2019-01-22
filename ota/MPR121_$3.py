default, 16uA charge current
			self._register8( 93, 0x20) # 0.5uS encoding, 1ms period
			# Enable all electrodes.
			self._register8( 94, 0x8F) # start with first 5 bits of baseline tracking
			# All done, everything succeeded!
			print('[MPR121] -> Reset successful')
			self.error = False
		except Exception:
			pass 
		return True

	def set_thresholds(self, touch, release, electrode=None):
		"""Sets the touch and release thresholds (0-255) for a single electrode (0-11) or all electrodes"""
		if not 0 <= touch <= 255:
			raise ValueError('Touch must be in range 0-255.')
		if not 0 <= release <= 255:
			raise ValueError('Release must be in range 0-255.')
		f = 0 if electrode is None else electrode
		t = 12 if electrode is None else electrode + 1

		# you can only modify the thresholds when in stop mode
		config = self._register8(94)
		if config != 0:
			self._register8(94, 0)

		for i in range(f, t):
			self._register8(65 + i * 2, touch)
			self._register8(66 + i * 2, release)

		# re