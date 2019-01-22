elf.hal_write_command(0x04 | 0x02)
		self.hide_cursor()
		self.display_on()
		cmd = 0x20
		if self.num_lines > 1:
			cmd |= 0x08
		self.hal_write_command(cmd)

	def clear(self):
		self.hal_write_command(0x01)
		self.hal_write_command(0x02)
		self.cursor_x = 0
		self.cursor_y = 0

	def show_cursor(self):
		self.hal_write_command(0x08 | 0x04 | 0x02)

	def hide_cursor(self):
		self.hal_write_command(0x08 | 0x04)

	def blink_cursor_on(self):
		self.hal_write_command(0x08 | 0x04 | 0x02 | 0x01)

	def blink_cursor_off(self):
		self.hal_write_command(0x08 | 0x04 |0x02)

	def display_on(self):
		self.hal_write_command(0x08 | 0x04)

	def display_off(self):
		self.hal_write_command(0x08)

	def backlight_on(self):
		self.backlight = True
		self.hal_backlight_on()

	def backlight_off(self):
		self.backlight = False
		self.hal_backlight_off()

	def move_to(self, cursor_x, cursor_y):
		self.cursor_x = cursor_x
		self.cursor_y = cursor_y
		addr = cursor_x & 0x3f
		if cursor_y & 1:
			addr += 0x40	# Li