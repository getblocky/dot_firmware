ap->' , end = '')
		self.wlan_sta.active(True)
		
		networks = []
		raw = self.wlan_sta.scan()
		for nw in raw:
			networks.append({'ssid': nw[0], 'rssi': nw[3]})
		content = core.json.dumps(networks).encode('utf-8')
		print(content)
		print(len(networks) , len(content) , type(content) , 'networks detected')
		httpResponse.WriteResponseOk(headers = None,contentType= "application/json",contentCharset = "UTF-8",content = content)
		
	async def Start(self):
		
		#This function will run config boot mode in background ! 
		#As an replacement for ConfigManager.py
		#When a network call is erro , it will create this task in 
		#main thread as an async function 
		#As such , this won't block
		
		core.gc.collect()
		if core.gc.mem_free() < 20000 :
			core.machine.reset()
		
		import hashlib #avoid concurrent unique_id 
		id = core.binascii.hexlify(hashlib.sha1(core.binascii.hexlify(core.machine.unique_id()).decode('ascii')).digest()[0:6]).decode('ascii')
		uuid = [id[i:i+2] for i in range(0, l