#version=1.0
import sys;core = sys.modules['Blocky.Core']

class I2cLcd():
	def __init__(self, i2c, i2c_addr, num_lines, num_columns):
		self.i2c = i2c
		self.i2c_addr = i2c_addr
		self.num_lines = num_lines
		if self.num_lines > 4:
			self.num_lines = 4
		self.num_columns = num_columns
		if self.num_columns > 40:
			self.num_columns = 40
		self.cursor_x = 0
		self.cursor_y = 0
		self.backlight = True
		try :
			self.init()
		except :
			pass
	def init(self):
		self.i2c.writeto(self.i2c_addr, bytearray([0]))
		core.time.sleep_ms(20)   # Allow LCD time to powerup
		# Send reset 3 times
		self.hal_write_init_nibble(0x30)
		core.time.sleep_ms(5)	# need to delay at least 4.1 msec
		self.hal_write_init_nibble(0x30)
		core.time.sleep_ms(1)
		self.hal_write_init_nibble(0x30)
		core.time.sleep_ms(1)
		# Put LCD into 4 bit mode
		self.hal_write_init_nibble(0x20)
		core.time.sleep_ms(1)
		#LcdApi.__init__(self, num_lines, num_columns)
		self.display_off()
		self.backlight_on()
		self.clear()
		s