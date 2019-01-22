turn to previous mode if temporarily entered stop mode
		if config != 0:
			self._register8(94, config)

	def filtered_data(self, electrode):
		"""Returns filtered data value for the specified electrode (0-11)"""
		if not 0 <= electrode <= 11:
			raise ValueError('Electrode must be in range 0-11.')
		return self._register16(4 + electrode * 2)

	def baseline_data(self, electrode):
		"""Returns baseline data value for the specified electrode (0-11)"""
		if not 0 <= electrode <= 11:
			raise ValueError('Electrode must be in range 0-11.')
		return self._register8(30 + electrode) << 2

	def touched(self):
		"""Returns a 12-bit value representing which electrodes are touched. LSB = electrode 0"""
		try :
			value =  self._register16(0)
			return value
		except :
			self.error = True
			return 0

	def is_touched(self, electrode):
		"""Returns True when the specified electrode is being touched"""
		if not 0 <= electrode <= 11:
			raise ValueError('Electrode must be in range 0-11.')
		t = self.