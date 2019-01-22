nes 1 & 3 add 0x40
		if cursor_y & 2:
			addr += 0x14	# Lines 2 & 3 add 0x14
		self.hal_write_command(0x80 | addr)

	def putchar(self, char):
		if char != '\n':
			self.hal_write_data(ord(char))
			self.cursor_x += 1
		if self.cursor_x >= self.num_columns or char == '\n':
			self.cursor_x = 0
			self.cursor_y += 1
			if self.cursor_y >= self.num_lines:
				self.cursor_y = 0
			self.move_to(self.cursor_x, self.cursor_y)

	def putstr(self, string):
		for char in string:
			self.putchar(char)

	def custom_char(self, location, charmap):
		location &= 0x7
		self.hal_write_command(0x40 | (location << 3))
		core.time.sleep_us(40)
		for i in range(8):
			self.hal_write_data(charmap[i])
			core.time.sleep_us(40)
		self.move_to(self.cursor_x, self.cursor_y)

	def hal_backlight_on(self):
		pass

	def hal_backlight_off(self):
		pass

	def hal_write_command(self, cmd):
		raise NotImplementedError

	def hal_write_data(self, data):
		raise NotImplementedError

	def hal_write_init_nibble(self, nibble)