 or data[x:x+1].isalpha() or data[x:x+1].isdigit():
					prefix += data[x:x+1]
		self._liRequest = prefix
		state(REQUEST,1)
		start_time = ticks_ms()
		await self.write((b'AT' if data.startswith(b'+') else b'')+data+(b'\r\n' if data.startswith(b'+') else b''))
		self.polling = True
		while isinstance(self._liRequest,bytes):
			self.parsing()
			while self.uart.any() == 0:
				await asyncio.sleep_ms(10)
				if ticks_diff(ticks_ms() , start_time) > timeout :
					raise OSError
			while self.uart.any() > 0:
				self.buffer += self.uart.read()
				await asyncio.sleep_ms(10)
			self.parsing()

		self.running = False
		self.polling = False
		state(REQUEST,0)
		print('[request] {} == {}'.format(prefix,self._liRequest))
		return self._liRequest

	async def waitfor(self,data,timeout=10000):
		timeout = 10000
		if isinstance(data,bytearray):
			data = bytes(data)
		elif isinstance(data,str):
			data = bytes(data,'utf-8')
		elif isinstance(data,bytes):
			data = data
		else :
			return

		state(