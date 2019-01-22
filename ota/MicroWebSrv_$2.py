		self._routeHandlers = routeHandlers
		self._srvAddr		 = (bindIP, port)
		self._webPath		 = webPath
		self._notFoundUrl	 = None
		self._started		 = False
		self.MaxWebSocketRecvLen	 = 1024
		self.WebSocketThreaded		 = True
		self.AcceptWebSocketCallback = None
		self.success = False
		self._socket = None 
		self.bootdone = False
	# ===( Server Process )=======================================================
	
	async def _socketProcess(self) :
		try :
			self._started = True
			wlan_ap = core.network.WLAN(core.network.AP_IF)
			wlan_ap.active(True)
			print('START AP')
			while True :
				await core.asyncio.sleep_ms(50)
				
				if wlan_ap.isconnected() and self.success == False:
					try :
						try :
							client, cliAddr = self._socket.accept()
						except :
							continue
						print(client , cliAddr)
						print('socket->Accepted')
						a = self._client(self, client, cliAddr)
						a._processRequest()
					except Exception as err :
						print('client->',err)
						core.sys.pr