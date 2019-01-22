			
	
	def volume(self , volume = None ):
		if volume == None :
			return self._readRegister(0x43)
		else :
			try :
				volume = max(0,min(30,int(volume)))
				self.sendStack(0x06 , 0x00 , volume)
			except :
				return 
	
	def loop ( self , song):
		try :
			song = max(0,int(song))
			self.sendStack(0x08, song//256 , song%256)
		except :
			pass
			
	def setEqualizer(self , eq):
		self.sendStack(0x07 , 0x00 , eq)
		
	def outputDevice( self , device):
		self.sendStack(0x09,0x00,device)
		time.sleep_ms(200)
	def sleep(self):
		self.sendStack(0x0A, 0x00,0x00)
	def reset(self):
		self.sendStack(0x0C,0x00,0x00)
		time.sleep_ms(2000)
	def start(self):
		self.sendStack(0x0D,0x00,0x00)
	def pause(self):
		self.sendStack(0x0E,0x00,0x00)
	def playFolder(self,folder,song):
		self.sendStack(0x0F,folder,song)
	def outputSetting(self,enable,gain):
		self.sendStack(0x10,enable,gain)
	def enableLoopAll(self):
		self.sendStack(0x11,0x00,0x01)
	def disableLoopAll(self):
		self.sendStack(0x11,0x00,0x00