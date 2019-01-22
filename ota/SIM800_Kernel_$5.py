os == -1 :
				print('[checkthis_1]',self.buffer)
				return
			string = self.buffer[0:pos]
			self._string = string
			self.buffer = self.buffer[len(string):]
			if len(string) == 0 and len(self.buffer) > 0 :
				string = self.buffer.lstrip()
				self.buffer = b''
			if len(string) == 0 or string in [b'\r',b'\n',b'\r\n']:
				continue
			# patch
			if len(self.buffer.strip()) == 0:
				self.buffer = b''
			self.belonged = False
			self._jCommand(string)
			self._jRequest(string)
			self._jEvent(string)
			if self.belonged == False:
				print('[unknown]',string)


	def _jEvent(self,data):
		if self.belonged:
			return
		data = data.lstrip()
		for key in self._liEvent.keys():
			if data.find(key) > -1 :
				print('[event] -> [{}] == {}'.format(key,data))
				self.belonged = True
				if data == key :
					self._liEvent[key] = True
				else :
					if data.find(b': ') > -1:
						data = data.split(b': ')[1].split(b',')
						for x in range(len(data)):
							try:
								data[x] = int(data