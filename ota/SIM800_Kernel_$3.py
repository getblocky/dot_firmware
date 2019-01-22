EVENT,1)
		start_time = ticks_ms()
		self._liEvent[data] = None
		while self._liEvent[data] == None :
			await asyncio.sleep_ms(10)
			if ticks_diff(ticks_ms() , start_time) > timeout :
				raise OSError('wait too lone' , data)

		print('[event]\t{}=={}'.format(data,self._liEvent[data]))
		state(EVENT,0)
		return self._liEvent.pop(data)

	async def command(self,data,response=[b'OK',b'ERROR'],timeout=1000):
		while self.running == True :
			await asyncio.sleep_ms(10)
		self.running = True
		self._liCommand = response

		for x in range(len(self._liCommand)):
			if isinstance(self._liCommand[x],bytearray):
				self._liCommand[x] = bytes(self._liCommand[x])
			elif isinstance(self._liCommand[x],str):
				self._liCommand[x] = bytes(self._liCommand[x],'utf-8')
			elif isinstance(self._liCommand[x],bytes):
				self._liCommand[x] = self._liCommand[x]

		state(COMMAND,1)

		await self.write((b'AT' if data.startswith(b'+') else b'')+data+(b'\r\n' if data.startswith(b'+') else b''))
		self.pollin