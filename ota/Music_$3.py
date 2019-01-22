)
	def playMP3Folder(self,file):
		self.sendStack(0x12,file//256,file%256)
	def advertise( self,file):
		self.sendStack(0x13,file//256,file%256)
	def stopAdvertise(self):
		self.sendStack(0x15)
		self.sendStack(0x16,0x00,0x00)
	def stop(self):
		self.sendStack(0x16,0x00,0x00)
	def loopFolder(self,folderNumber):
		self.sendStack(0x17, folderNumber//256,folderNumber%256)
	def randomAll(self):
		self.sendStack(0x18,0x00,0x00)
	def enableLoop(self):
		self.sendStack(0x19, 0x00,0x00)
	def disableLoop(self):
		self.sendStack(0x19, 0x01,0x00)
	def enableDAC(self):
		self.sendStack(0x1A, 0x00,0x00)
	def disableDAC(self):
		self.sendStack(0x1A, 0x01,0x00)
	def readState(self):
		return self._readRegister(0x42)
	def readEQ(self):
		return self._readRegister(0x44)
	def readFileCounts(self):
		return self._readRegister(0x48)
	def readCurrentFileNumber(self):
		return self._readRegister(0x4C)
	def readFileCountsInFolder(self,folder):
		return self._readRegister(0x4E,folder)
	def readFolderCounts(se