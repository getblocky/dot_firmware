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
								#await core.indicato