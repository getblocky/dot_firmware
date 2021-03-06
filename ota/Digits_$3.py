			sleep_us(TM1637_DELAY)
		self.clk(0)
		sleep_us(TM1637_DELAY)
		self.clk(1)
		sleep_us(TM1637_DELAY)
		self.clk(0)
		sleep_us(TM1637_DELAY)

	def brightness(self, val=None):
		"""Set the display brightness 0-7."""
		# brightness 0 = 1/16th pulse width
		# brightness 7 = 14/16th pulse width
		if val is None:
			return self._brightness
		if not 0 <= val <= 7:
			raise ValueError("Brightness out of range")

		self._brightness = val
		self._write_data_cmd()
		self._write_dsp_ctrl()

	def write(self, segments, pos=0):
		"""Display up to 6 segments moving right from a given position.
		The MSB in the 2nd segment controls the colon between the 2nd
		and 3rd segments."""
		if not 0 <= pos <= 5:
			raise ValueError("Position out of range")
		self._write_data_cmd()
		self._start()

		self._write_byte(TM1637_CMD2 | pos)
		for seg in segments:
			self._write_byte(seg)
		self._stop()
		self._write_dsp_ctrl()

	def encode_digit(self, digit):
		"""Convert a character 0-9, a-f to a segment."""
		re