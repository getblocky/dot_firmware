s, max(self.min_us, us))
		duty = us * 1024 * self.freq // 1000000
		try :
			self.pwm.duty(int(duty))
		except :
			pass

	def angle(self, degrees=None, radians=None):
		"""Move to the specified angle in ``degrees`` or ``radians``."""
		if degrees == None and radians == None :
			return self.currentAngle
			
		if degrees is None:
			degrees = math.degrees(radians)
		self.currentAngle = degrees
		degrees = degrees % 360
		total_range = self.max_us - self.min_us
		us = self.min_us + total_range * degrees // self.maxAngle
		self.write_us(us)

	def deinit(self):
		self.pwm.duty(0)
		self.pwm.deinit()
		Pin(self.p[0],Pin.IN)
