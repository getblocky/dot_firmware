+= await self.conn.recv(length)
			else :
				self._rx_data += self.conn.recv(length)
			
		except OSError as err:
			if err.args[0]==errno.ETIMEDOUT:
				return b''
			elif err.args[0] == errno.EAGAIN:
				return b''
			else :
				core.flag.blynk = False
				print('[BLYNK] Cant receive data , resetting blynk')
		if len(self._rx_data) >= length:
			data = self._rx_data[:length]
			self._rx_data = self._rx_data[length:]
			#print('[Blynk] Receiving ' , data)
			return data
		else :
			return b''
			
	async def _send(self,data):
		#print('[Blynk] Sending ' , data)
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
			self.conn.close()
		self.state = DISCONNECTED
		await core.wait(RECONNECT_DELAY)
		if emsg:
			print('[BLYNK] Error: {}, connection closed'.format(emsg))
	
	async def _server_alive(self):
		c_time = core.Timer.runtime()
		if self._m_time != c_time:
			self._m_time = c_time
			self._tx_count = 0
			if self._last_hb_id != 0 and c_time - self._hb_time >= MAX_SOCK_TO:
				return False
			
			if c_time - self._hb_time >= HB_PERIOD and self.state == AUTHENTICATED:
				self._hb_time = c_time
				self._last_hb_id = self._new_msg_id()
				await self._send(core.struct.pack(HDR_FMT,MSG_PING,self._last_hb_id,0))
		return True		
		
	async def notify(self,msg):
		if self.state == AUTHENTICATED:
			await self._send(self._format_msg(MSG_NOTIFY, msg))
	
	async def tweet(self, msg):
		if self.state == AUTHENTICATED:
			await self._send(self._format_msg(MSG_TWEET, msg))

	async def email(self, email, subject, content):
		if se