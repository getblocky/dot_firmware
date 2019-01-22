	contentType	 = "text/html",
				contentCharset = "UTF-8",
				content = 'Failed')
		
		"""
		if self.wifi_status == 1:
			print('Wait for rebooting')
			time.sleep(5)
			print('Rebooting')
			machine.reset()
		"""

	def _httpHandlerSaveConfig(self, httpClient, httpResponse):
		self.request_json  = ''
		self.request_json = core.json.loads(httpClient.ReadRequestContent().decode('ascii'))
		self.wifi_status = 0
		httpResponse.WriteResponseOk(headers = None,contentType= "text/html",	contentCharset = "UTF-8",content = 'OK')
		self.wlan_sta.connect(self.request_json['ssid'], self.request_json['password'])
		
		#
		while not self.wlan_sta.isconnected() :
			core.time.sleep_ms(100)
			print('.',end = '')
		#
		
		print('client->saveconfig: Trying to connect to ' + str(self.request_json) , end = '')
		# we cant wait until the network to be connect here !
	def is_ascii(self, s):
		return all(ord(c) < 128 for c in s)
	
	def _httpHandlerScanNetworks(self, httpClient, httpResponse) :
		print('scan