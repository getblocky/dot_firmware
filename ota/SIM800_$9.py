 self.state == AUTHENTICATED:
			await self._send(self._format_msg(MSG_HW_SYNC))

	async def sync_virtual(self, pin):
		if self.state == AUTHENTICATED:
			await self._send(self._format_msg(MSG_HW_SYNC, 'vr', pin))
	
	async def sending(self,to,data):
		await self._send(self._format_msg(MSG_HW,'vw',pin,val))
		
	async def run(self):
		self._start_time = ticks_ms()
		self._task_millis = self._start_time
		self._hw_pins = {}
		self._rx_data = b''
		self._msg_id = 1
		self._timeout = None
		self._tx_count = 0
		self._m_time = 0
		self.state = DISCONNECTED
		
		if not self._ext_socket:
			while not wifi.wlan_sta.isconnected():
				self.last_call = ticks_ms()
				await asyncio.sleep_ms(500)
		while True :
			self._start_time = ticks_ms()
			self.last_call = ticks_ms()
			# Connecting to Blynk Server
			while self.state != AUTHENTICATED:
				try:
					self.last_call = ticks_ms()
					await asyncio.sleep_ms(100)
					gc.collect()
					print('[Blynk] Connecting')
					self.state = CONNECTING
					
					if not self._ext_socket :
						print('TCP: Connting to {} : {}'.format(self._server,self._port))
						self.conn = socket.socket() 
						self.conn.settimeout(1)
					else :
						while ext_socket == None:
							await asyncio.sleep_ms(500)
						self.conn = ext_socket
						await self.conn.settimeout(0.1)
					while True :
						try :
							if not self._ext_socket:
								b = socket.getaddrinfo(self._server,self._port)[0][4]
								self.conn.connect(b)
								break
							else :
								await self.conn.connect(self._server,self._port)
								break
						except OSError as err:
							import sys;sys.print_exception(err)
							print('>')
							await asyncio.sleep_ms(5000)
							continue
					print('Socket: Connected at {}'.format(ticks_ms()))
				except Exception as err:
					import sys
					sys.print_exception(err)
					await self._close('connection with the Blynk servers failed')
					break
				
				self.state = AUTHENTICATING
				hdr = struct.pack(HDR_FMT, MSG_LOGIN, 