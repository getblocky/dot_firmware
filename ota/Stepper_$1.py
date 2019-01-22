ep=1 , speed = 1):
		if direction == 'clockwise':self.target = self.current + step
		if direction == 'counter-clockwise':self.target = self.current - step
		
		while self.current != self.target:
			self.handler()
		
		
	def handler(self):
		
		self.current = self.current + 1 if self.current < self.target else self.current - 1
		
		if self.target > self.current :
			for x in range(8):
				self.set(x);sleep_ms(1)
		if self.target < self.current:
			for x in range(7,-1,-1):
				self.set(x);sleep_ms(1)
      
			
		
	def get(self):
		return self.current 
		

		
		
		
		
		
