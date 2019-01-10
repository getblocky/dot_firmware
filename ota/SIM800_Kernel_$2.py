	
	def trigger (self,kw,func):
		pass
	def parsing(self):
		if self.buffer.startswith(self.echo):
			self.buffer = self.buffer[len(self.echo):]
			self.echo = b''
		for x in self.buffer.splitlines():
			if len(x)>0:
				print('\t\t\t[PARSE]\t\t' ,x,end='')
				self.belonged = False
				self._jCommand(x)
				self._jRequest(x)
				self._jEvent(x)
				if self.belonged == False :
					print('< unknown >')
		if self.cleanup == True :
			self.buffer = b''
	def _jEvent	(self,data):
		if self.belonged :
			return
		for key in self._liEvent.keys():
			if data.find(key) > -1:
				print('Event {} Received as {}'.format(key,data))
				self.belonged = True
				rep = data.split(b': ')[1].split(b',')
				for x in range(len(rep)):
					try :
						rep[x] = int(rep[x])
					except ValueError:
						pass
				self._liEvent[key] = rep
		pass
	def _jCommand(self,data):
		if self.belonged :
			return
		if isinstance(self._liCommand,list) and data in self._liCommand:
			self._liCommand = self._liCommand.index(data)
			print('\t\t[COMMAND] Returned\t' , data , 'index=',self._liCommand)
			self.belonged = True
			
	def _jRequest(self,data):
		# some request response may not have "+" symbol
		# we use regex for this stuff
		if self.belonged :
			return
		if self._liRequest == None :
			return
		elif type(self._liRequest) == type(re.compile('')):
			pass
		elif isinstance(self._liRequest,bytes) and self._liRequest.startswith(b'*'):
			if self._liRequest == b'*':
				self._liRequest = [data]
			else :
				self._liRequest = self._liRequest[1:]
				self.belonged = True
		elif isinstance(self._liRequest,bytes):
			if data.startswith(self._liRequest):
				data = data[len(self._liRequest):]
				data = data.replace(b':',b'')
				data = data.split(b',')
				for x in range(len(data)):
					try :
						data[x] = int(data[x])
					except ValueError:
						pass
				print('\t\t[REQUEST] Returned : {}'.format(self._liRequest) , '=',data)
				self.belonged = True
				self._liRequest = data	
		
	async def co