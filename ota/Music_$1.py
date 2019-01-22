top = 1 , rx = self.p[0] , tx = self.p[1] )
		
		nowTime = time.ticks_ms()
		while self.bus.any() :
			self.bus.read()
			
		if param == None :
			self.sendStack(cmd,0x00,0x00)
		else :
			self.sendStack(cmd,param//256,param%256)
		while not self.bus.any():
			if time.ticks_diff(time.ticks_ms() , nowTime) > 200:
				return None
		buffer = self.bus.read(10)
		print('RECV : ',end='')
		for x in buffer:
			print(hex(x),end = '\t')
		print()
		
		return buffer[5]*256 + buffer[6]
		
	#=====================================================
	def nextSong(self):
		self.sendStack(0x01,0x00,0x00)
	def previousSong(self):
		self.sendStack(0x02,0x00,0x00)
	def play( self , song , folder = None ):
		if folder == None :
			try :
				song = max(0,int(song))
				self.sendStack(0x03, song//256 , song%256)
			except Exception as err:
				print(err)
				return 
			
		else :
			try :
				song = max(0,int(song))
				folder = max(0,int(folder))
				self.sendStack(0x0F, folder , song)
			except :
				return 
