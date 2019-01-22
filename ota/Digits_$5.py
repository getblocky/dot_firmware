mat(val & 0xffff)
		self.write(self.encode_string(string))

	def number(self, num):
		"""Display a numeric value -999 through 9999, right aligned."""
		# limit to range -999 to 9999
		num = max(-999, min(num, 9999))
		string = '{0: >4d}'.format(num)
		self.write(self.encode_string(string))

	def numbers(self, num1, num2, colon=True):
		"""Display two numeric values -9 through 99, with leading zeros
		and separated by a colon."""
		num1 = max(-9, min(num1, 99))
		num2 = max(-9, min(num2, 99))
		segments = self.encode_string('{0:0>2d}{1:0>2d}'.format(num1, num2))
		if colon:
			segments[1] |= 0x80 # colon on
		self.write(segments)

	def temperature(self, num):
		if num < -9:
			self.show('lo') # low
		elif num > 99:
			self.show('hi') # high
		else:
			string = '{0: >2d}'.format(num)
			self.write(self.encode_string(string))
		self.write([_SEGMENTS[38], _SEGMENTS[12]], 2) # degrees C

	def show(self, string, colon=False):
		segments = self.encode_string(string)
		if len(segments) > 1 and