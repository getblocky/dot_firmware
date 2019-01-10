cket :
			await self.conn.close()
		else :
			self.conn.close()
		self.state = DISCONNECTED
		await asyncio.sleep_ms(RECONNECT_DELAY)
		if emsg:
			print('[BLYNK] Error: {}, connection closed'.format(emsg))
	
	async def _server_alive(self):
		c_time = ticks_ms()
		if self._m_time != c_time:
			self._m_time = c_time
			self._tx_count = 0
			if self._last_hb_id != 0 and c_time - self._hb_time >= MAX_SOCK_TO:
				return False
			
			if c_time - self._hb_time >= HB_PERIOD and self.state == AUTHENTICATED:
				self._hb_time = c_time
				self._last_hb_id = self._new_msg_id()
				await self._send(struct.pack(HDR_FMT,MSG_PING,self._last_hb_id,0))
		return True		
		
	async def notify(self,msg):
		if self.state == AUTHENTICATED:
			await self._send(self._format_msg(MSG_NOTIFY, msg))
	
	async def tweet(self, msg):
		if self.state == AUTHENTICATED:
			await self._send(self._format_msg(MSG_TWEET, msg))

	async def email(self, email, subject, content):
		if self.state == AUTHENTICATED:
			await self._send(self._format_msg(MSG_EMAIL, email, subject, content))

	async def virtual_write(self,pin,val,device = None):
		if self.state == AUTHENTICATED:
			if device == None:
				await self._send(self._format_msg(MSG_HW, 'vw', pin, val))
			else : 
				await self._send(self._format_msg(MSG_BRIDGE ,124, 'i' , device)) # Set channel V124 of this node to point to that device
				await self._send(self._format_msg(MSG_BRIDGE, 124,'vw',  pin , val))
				
	async def set_property(self, pin, prop, val):
		if self.state == AUTHENTICATED:
			await self._send(self._format_msg(MSG_PROPERTY, pin, prop, val))

	async def log_event(self, event, descr=None):
		if self.state == AUTHENTICATED:
			if descr==None:
				await self._send(self._format_msg(MSG_EVENT_LOG, event))
			else:
				await self._send(self._format_msg(MSG_EVENT_LOG, event, descr))
				
	async def log(self,message):
		await self.virtual_write(device = self._token.decode('utf-8') , pin = 127 , val = message )
		
	async def sync_all(self):
		if