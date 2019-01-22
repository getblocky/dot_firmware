[x])
							except ValueError:
								pass
						self._liEvent[key] = data

	def _jCommand(self,data):
		if self.belonged:
			return
		data = data.lstrip()
		if isinstance(self._liCommand,list) and data in self._liCommand:
			self._liCommand = self._liCommand.index(data)
			print('[command] [{}] == {}'.format(data,self._liCommand))
			self.belonged = True

	def _jRequest(self,data):
		if self.belonged:
			return
		data = data.lstrip()
		if self._liRequest == None :
			return
		elif isinstance(self._liRequest,bytes) and self._liRequest.startswith(b'*'):
			if self._liRequest == b'*':
				self._liRequest = [data]
			else :
				self._liRequest = self._liRequest[1:]
			self.belonged = True
		elif isinstance(self._liRequest,bytes) and not self._liRequest.startswith(b'*'):
			if data.startswith(self._liRequest):
				data = data[len(self._liRequest):]
				data = data.replace(b':',b'').split(b',')
				for x in range(len(data)):
					try :
						data[x] = int(data[x])
					except ValueError:
	