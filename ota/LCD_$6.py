rue
			pass
	def deinit(self):
		self.clear()
		Pin(self.p[0],Pin.IN)
		Pin(self.p[1],Pin.IN)
