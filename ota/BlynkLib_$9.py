lf.state == AUTHENTICATED:
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
					core.gc.collect()
					core.indicator.show('b