 None :
							await self.log('[REPR] {}'.format(repr(out)))
					except:
						try :
							exec(params[0])
						except Exception as err:
							await self.log('[EXCEPTION] {}'.format(repr(e)))
				
				# OTA Channel
				elif pin == 126 :
					print('[{}] OTA Message Received'.format(ticks_ms()))
					gc.collect()
					ota_lock = eeprom.get('OTA_LOCK')
					if (ota_lock==True and cfn_btn.value()==0)or ota_lock != True :
						if ota_file == None:
							ota_file = open('temp_code.py','w')
							ota_file.write(prescript)
						if params[1] == 'OTA':
							await asyn.Cancellable.cancel_all()
							await cleanup()
							await self.log('[OTA_READY]')
						elif params[1] == "[OTA_CANCEL]":
							if ota_file:
								ota_file.flush()
								ota_file.close()
						else :
							total_part = int(params[1].split('/')[1])
							curre_part = int(params[1].split('/')[0])
							sha1 = binascii.hexlify(hashlib.sha1(params[0]).digest()).decode('utf-8')
							print('[PART {}/{} , length = {} , sha1 = {}'.format(curre_part,total_part,len(params[0]),sha1))
							if total_part == curre_part:
								ota_file.write(params[0])
								ota_file.flush()
								ota_file.close()
								ota_file = None
								os.rename('temp_code.py','user_code.py')
								await self.log('[OTA_ACK]' + str([sha1,params[1]]))
								await self.log('[OTA_DONE]')
								print('user code saved')
								for x in range(50):
									await asyncio.sleep_ms(1)
								for x in range(50,-1,-1):
									await asyncio.sleep_ms(1)											
								mainthread.call_soon(self.ota())
							if curre_part < total_part:
								progress = int(curre_part)%13
								total = int(total_part)%13
								total = 12 if total_part - curre_part > 12 else total
								ota_file.write(params[0])
								ota_file.flush()
								await self.log('[OTA_ACK]'+str([sha1,params[1]]))
								
					else :
						await self.log('[DOT_ERROR] OTA_LOCKED')
				
				# User defined channel
				# Note that "vr" and "vw" is the sa