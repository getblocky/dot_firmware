_ssid = None
				for n in config['known_networks']:
					if n['ssid'] == self.request_json['ssid']:
						exist_ssid = n
						break
				if exist_ssid:
					exist_ssid['password'] = self.request_json['password'] # update WIFI password
					print('Update wifi password')
				else:
					# add new WIFI network
					config['known_networks'].append({'ssid': self.request_json['ssid'], 'password': self.request_json['password']})
					print('Add new network')
			if len(self.request_json['token']):
				config['token'] = self.request_json['token']
			
			f = open('config.json', 'w')
			f.write(core.json.dumps(config))
			f.close()
			core.flag.wifi = True
			print('Get check status request ->',end = '')
			
			httpResponse.WriteResponseOk(headers = None,
				contentType	 = "text/html",
				contentCharset = "UTF-8",
				content = 'OK')
			print('completed')
			self.server.setup_success()
		else :
			core.flag.wifi = False
			print('.' , end = '')
			httpResponse.WriteResponseOk(headers = None,
			