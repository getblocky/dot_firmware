		self.p = getPort(port)
		
		self.clk =Pin(self.p[0])
		self.dio = Pin(self.p[1])

		if not 0 <= brightness <= 7:
			raise ValueError("Brightness out of range")
		self._brightness = brightness

		self.clk.init(Pin.OUT, value=0)
		self.dio.init(Pin.OUT, value=0)
		sleep_us(TM1637_DELAY)

		self._write_data_cmd()
		self._write_dsp_ctrl()

	def _start(self):
		self.dio(0)
		sleep_us(TM1637_DELAY)
		self.clk(0)
		sleep_us(TM1637_DELAY)

	def _stop(self):
		self.dio(0)
		sleep_us(TM1637_DELAY)
		self.clk(1)
		sleep_us(TM1637_DELAY)
		self.dio(1)

	def _write_data_cmd(self):
		# automatic address increment, normal mode
		self._start()
		self._write_byte(TM1637_CMD1)
		self._stop()

	def _write_dsp_ctrl(self):
		# display on, set brightness
		self._start()
		self._write_byte(TM1637_CMD3 | TM1637_DSP_ON | self._brightness)
		self._stop()

	def _write_byte(self, b):
		for i in range(8):
			self.dio((b >> i) & 1)
			sleep_us(TM1637_DELAY)
			self.clk(1)
			sleep_us(TM1637_DELAY)
			self.clk(0)
