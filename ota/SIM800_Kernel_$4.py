g = True
		start_time = ticks_ms()
		while not isinstance(self._liCommand,int):
			self.parsing()
			while self.uart.any() == 0:
				await asyncio.sleep_ms(10)
				if ticks_diff(ticks_ms(),start_time) > timeout :
					raise OSError("Timeout " , data)
			while self.uart.any() > 0:
				self.buffer += self.uart.read()
				await asyncio.sleep_ms(10)
			self.parsing()

		self.polling = False
		self.running = False
		state(COMMAND,0)
		print('[command] {} == {}'.format(data,self._liCommand))
		return self._liCommand

	async def write(self,data):
		self.echo = data[0:-1]
		if self.uart.any() > 0 :
			self.buffer += self.uart.read()
		if len(self.buffer):
			self.parsing()
		else :
			self.uart.write(data)
			print('[write] {}'.format(data))


	def parsing(self):
		if self.buffer.startswith(self.echo):
			self.buffer = self.buffer[len(self.echo):]
			self.echo = b''
		while len(self.buffer) > 0 :

			pos = max((self.buffer.find(b'\r\n'),self.buffer.find(b'\r'),self.buffer.find(b'\n')))
			if p