ore
			try :
				if self._ext_socket :
					self._rx_data += await self.conn.recv(length)
				else :
					self._rx_data += self.conn.recv(length)
			except OSError :
				return b''

		data = self._rx_data[:length]
		print('[blynk] , receiving ' , data , length , "==" , len(data))
		print(self._rx_data)

		self._rx_data = self._rx_data[length:]
		print(self._rx_data)
		print()
		return data

	async def _send(self,data):
		#print('[Blynk] Sending ' , data)
		print('>>> [_send]\t',data)
		retries = 0
		while retries <= MAX_TX_RETRIES:
			try :
				if self._ext_socket :
					await self.conn.send(data)
				else :
					self.conn.send(data)
				self._tx_count += 1
				break
			except OSError as err:
				if err.args[0] != errno.EAGAIN:
					core.flag.blynk = False
					print('[BLYNK] Problem sending data')
					retries += 1
					await core.wait(200)
				else :
					await core.wait(RE_TX_DELAY)

	async def _close(self,emsg=None):
		if self._ext_socket :
			await self.conn.close()
		else :
			se