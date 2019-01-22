dfrom_mem(self.address, register, 2)
			return core.struct.unpack("<H", data)[0]
		self.i2c.writeto_mem(self.address, register, core.struct.pack("<H", value))

	def reset(self):
		try :
			# Soft reset of device.
			
			self._register8( 128, 0x63)
			core.time.sleep_ms(1)
			self._register8( 94, 0x00)
			# Check CDT, SFI, ESI configuration is at default values.
			c = self._register8( 93)
			if c != 0x24:
			   return False
			# Set threshold for touch and release to default values.
			self.set_thresholds(12, 6)
			# Configure baseline filtering control registers.
			self._register8( 43, 0x01)
			self._register8( 44, 0x01)
			self._register8( 45, 0x0E)
			self._register8( 46, 0x00)
			self._register8( 47, 0x01)
			self._register8( 48, 0x05)
			self._register8( 49, 0x01)
			self._register8( 50, 0x00)
			self._register8( 51, 0x00)
			self._register8( 52, 0x00)
			self._register8( 53, 0x00)
			# Set other configuration registers.
			self._register8( 91, 0)
			self._register8( 92, 0x10) # 