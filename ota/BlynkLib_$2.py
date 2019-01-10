							for x in range(50):
									core.indicator.rgb.fill((0,x,0));core.indicator.rgb.write()
									await core.wait(1)
								for x in range(50,-1,-1):
									core.indicator.rgb.fill((0,x,0));core.indicator.rgb.write()
									await core.wait(1)											
								core.mainthread.call_soon(self.ota())
							if curre_part < total_part:
								progress = int(curre_part)%13
								total = int(total_part)%13
								total = 12 if total_part - curre_part > 12 else total
								for x in range(total):
									core.indicator.rgb[x] = (25,0,0)
								for x in range(progress):
									core.indicator.rgb[x] = (0,25,0)
								core.indicator.rgb.write()
								core.ota_file.write(params[0])
								core.ota_file.flush()
								await self.log('[OTA_ACK]'+str([sha1,params[1]]))
								
					else :
						await self.log('[DOT_ERROR] OTA_LOCKED')
				
				# User defined channel
				# Note that "vr" and "vw" is the same
				elif (str(pin) in self._vr_pins):
					self.message = params
					for x in range(len(self.message)):
						try :
							self.message[x] = int(self.message[x])
						except :
							pass
					if len(self.message) == 1:
						self.message = self.message[0]
					print('[BLYNK] V{} {} -> {}'.format(pin,type(self.message),self.message))
					if callable(self._vr_pins[str(pin)]):
						await core.call_once('user_blynk_{}_vw'.format(pin),self._vr_pins[str(pin)])
				else :
					print('unregistered channel {}'.format(pin))
		except Exception as err:
			import sys;sys.print_exception(err)
			pass
	
	def _new_msg_id(self):
		self._msg_id +=1
		self._msg_id = 1 if self._msg_id > 0xFFFF else self._msg_id
		return self._msg_id
		
	async def _settimeout(self,timeout):
		if timeout != self._timeout:
			self._timeout = timeout
			if self._ext_socket :
				await self.conn.settimeout(timeout)
			else :
				self.conn.settimeout(timeout)
			
	async def _recv(self,length,timeout=0):
		await self._settimeout(timeout)
		try:
			if self._ext_socket :
				self._rx_data 