lf.conn.close()
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
		if self.state == AUTHENTICATED:
			await self._send(self._format_msg(MSG_EMAIL, email, subject,