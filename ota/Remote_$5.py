in range(self.length//8) :
			for i in range(8):
				print(self.buffer[x*8+i]*50 , end = "\t" if	self.buffer[x*8+i]*50 > 300 else "#\t")
			print()
		for x in range(self.length%8):
			print( self.buffer[self.length//8 + x]*50 , end = "\t" if	self.buffer[self.length//8 + x]*50 > 300 else "#\t")
			
		print("------------------------------------------")
		
		
		
	def _recvActive(self , state):
		if state == True :
			self.recv = core.machine.Pin(self.p[1] , core.machine.Pin.IN , core.machine.Pin.PULL_UP)
			self.recv.irq(trigger = core.machine.Pin.IRQ_RISING|core.machine.Pin.IRQ_FALLING , handler = self._handler)
		elif state == False :
			self.recv.irq(trigger = 0 , handler = None)
			self.recv = core.machine.Pin(self.p[1] , core.machine.Pin.IN)
		core.time.sleep_ms(5)
		
	def _store(self , name , packet , bin , length = None):
		meta_data = {"bin":bin , "length": length or len(packet) , "protocol" : "RAW"}
		with open("IR/{}.txt".format(name),"w") as fp :
			fp.write(core.json.dumps(met