lf.state == AUTHENTICATED:
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
		if self.state == AUTHENTICATED:
			await self._send(self._format_msg(MSG_HW_SYNC))

	async def sync_virtual(self, pin):
		if self.state == AUTHENTICATED:
			await self._send(self._format_msg(MSG_HW_SYNC, 'vr', pin))
	
	async def sending(self,to,data):
		await self._send(self._format_msg(MSG_HW,'vw',pin,val))
		
	async def run(self):
		self._start_time = core.Timer.runtime()
		self._task_millis = self._start_time
		self._hw_pins = {}
		self._rx_data = b''
		self._msg_id = 1
		self._timeout = None
		self._tx_count = 0
		self._m_time = 0
		self.state = DISCONNECTED
		
		if not self._ext_socket:
			while not core.wifi.wlan_sta.isconnected():
				self.last_call = core.Timer.runtime()
				await core.wait(500)
		while True :
			self._start_time = core.Timer.runtime()
			self.last_call = core.Timer.runtime()
			# Connecting to Blynk Server
			while self.state != AUTHENTICATED:
				try:
					self.last_call = core.Timer.runtime()
					await core.wait(100)
	