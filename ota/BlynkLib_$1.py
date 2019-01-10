r_pins[str(pin)] = write
		
	async def _handle_hw(self,data):
		print('[Blynk] : Handling data ')
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
						if params[1] == 'OTA':
							await core.asyn.Cancellable.cancel_all()
							await core.cleanup()
							await core.indicator.pulse(color = (0,15,25))
							await self.log('[OTA_READY]')
						elif params[1] == "[OTA_CANCEL]":
							if core.ota_file:
								core.ota_file.flush()
								core.ota_file.close()
						else :
							total_part = int(params[1].split('/')[1])
							curre_part = int(params[1].split('/')[0])
							sha1 = core.binascii.hexlify(core.hashlib.sha1(params[0]).digest()).decode('utf-8')
							print('[PART {}/{} , length = {} , sha1 = {}'.format(curre_part,total_part,len(params[0]),sha1))
							if total_part == curre_part:
								core.ota_file.write(params[0])
								core.ota_file.flush()
								core.ota_file.close()
								core.ota_file = None
								core.os.rename('temp_code.py','user_code.py')
								await self.log('[OTA_ACK]' + str([sha1,params[1]]))
								await self.log('[OTA_DONE]')
								print('user code saved')
								#await core.indicator.pulse(color = (0,50,0))
	