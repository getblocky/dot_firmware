t !=T:
				core.eeprom.set('EXT_SOCKET',T);core.machine.reset()
			if core.hardware['uart'].count(None)==0:
				raise Exception('no uart')
			self.i=core.hardware['uart'].index(None);self.u=UART(self.i,rx=self.p[0],tx=self.p[1]);core.hardware['uart'][self.i]=self
			while True:
				self.u.write('AT\r\n');ts(100)
				if self.u.any() > 0:
					a=self.u.read()
					if a.count(b'OK'):
						break
			core.ext_socket=self
			core.mainthread.create_task(self.rSMS());core.mainthread.create_task(self.connect());core.mainthread.create_task(self._routine());core.deinit_list.append(self)
	def deinit(self):
		core.hardware['uart'][self.i]=None
	def isconnected(self):
		return self.fc
	async def _routine(self):
		while T:
			await s(100)
			if self.fp==F and self.u.any():
				while self.u.any() > 0:
					self.b +=self.u.read()
				self.j()
	async def r(self,d,w=N,to=5000):
		d=b(d);w=b(w)
		while self.fr==T:
			await s(10)
		self.fr=T
		if w==N:
			w=b''
			for x in range(len(d)):
				if d[x:x+1] in