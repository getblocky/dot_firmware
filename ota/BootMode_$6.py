--------------------------------------
		
		#-------------------------------------------------
		self.wlan_sta.active(True)
		self.wlan_ap.active(True)
		
		self.wlan_ap.config(essid = ap_name , password = ap_password	)

		routeHandlers = [
			("/", "GET", self._httpHandlerIndexGet),
			("/aplist", "GET", self._httpHandlerScanNetworks),
			("/status", "GET", self._httpHandlerCheckStatus),
			("/save", "POST",	self._httpHandlerSaveConfig)
		]
		
		from Blocky.MicroWebSrv import MicroWebSrv
		self.server = MicroWebSrv(routeHandlers = routeHandlers)
		print('bootmode-> started')
		#loop = asyncio.get_event_loop()
		#loop.create_task(server.Start())
		
		await self.server.Start()
		print('bootmode-> completed')
			
		from machine import reset
		reset()
	


