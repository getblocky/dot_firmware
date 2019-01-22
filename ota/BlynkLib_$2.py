s[str(pin)] = write

	async def _handle_hw(self,data):
		print('[Blynk] : Handling data ')
		print('[{}]'.format(len(data)) , data)
		try :
			params = list(map(lambda x:x.decode('ascii'),data.split(b'\0')))
			cmd = params.pop(0)
			if cmd == 'vw' or cmd == 'vr':
				pin = int(params.pop(0))

				# Repr channel
				if pin == 127 :
					core.flag.direct_command = True
					try :
						out = eval(params[0])
						if out != None :
							await self.log('[REPR] {}'.format(repr(out)))
					except:
						try :
							exec(params[0])
						except Exception as err:
							await self.log('[EXCEPTION] {}'.format(repr(err)))

				# OTA Channel
				elif pin == 126 :
					print('[{}] OTA Message Received'.format(core.Timer.runtime()))
					core.gc.collect()
					ota_lock = core.eeprom.get('OTA_LOCK')
					if (ota_lock==True and core.cfn_btn.value()==0)or ota_lock != True :
						if core.ota_file == None:
							core.ota_file = open('temp_code.py','w')
							core.ota_file.write(core.prescript)
			