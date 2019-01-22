ta.active(False)
			return False
	def _httpHandlerIndexGet(self, httpClient, httpResponse):
		print('Get index request , memoryview' )
		# Heap fragmentation is our enemy
		f = open('Blocky/index.html')
		print('[bootmode] -> writing index request ',end='')
		content = []
		f = open('Blocky/index.html')
		while True:
			temp = f.read(500)
			if len(temp) == 0:
				break
			content.append(temp)
		f.close()
		httpResponse.WriteResponseOk( headers = None,contentType= "text/html",	contentCharset = "UTF-8",	content = content) 
		
		
	def _httpHandlerCheckStatus(self, httpClient, httpResponse):
		print('checking')
		if self.wlan_sta.isconnected():
			self.wifi_status = 1
			print('Connected to ' , self.request_json['ssid'])
			config = {}
			try :
				config = core.json.loads(open('config.json').read())
			except :
				pass
			if not config.get('known_networks'):
				config['known_networks'] = [{'ssid': self.request_json['ssid'], 'password': self.request_json['password']}]
			else:
				exist