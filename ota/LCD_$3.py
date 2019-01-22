:
		byte = ((nibble >> 4) & 0x0f) << 4
		self.i2c.writeto(self.i2c_addr, bytearray([byte | 0x04]))
		self.i2c.writeto(self.i2c_addr, bytearray([byte]))

	def hal_backlight_on(self):
		self.i2c.writeto(self.i2c_addr, bytearray([1 << 3]))

	def hal_backlight_off(self):
		self.i2c.writeto(self.i2c_addr, bytearray([0]))

	def hal_write_command(self, cmd):
		byte = ((self.backlight << 3) | (((cmd >> 4) & 0x0f) << 4))
		self.i2c.writeto(self.i2c_addr, bytearray([byte | 0x04]))
		self.i2c.writeto(self.i2c_addr, bytearray([byte]))
		byte = ((self.backlight << 3) | ((cmd & 0x0f) << 4))
		self.i2c.writeto(self.i2c_addr, bytearray([byte | 0x04]))
		self.i2c.writeto(self.i2c_addr, bytearray([byte]))
		if cmd <= 3:
			# The home and clear commands require a worst case delay of 4.1 msec
			core.time.sleep_ms(5)

	def hal_write_data(self, data):
		byte = (0x01 | (self.backlight << 3) | (((data >> 4) & 0x0f) << 4))
		self.i2c.writeto(self.i2c_addr, bytearray([byte | 0x04]))
		self.i2c.writeto(self.i2c