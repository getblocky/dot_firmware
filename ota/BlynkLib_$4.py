r.pulse(color = (0,50,0))
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
					self.message = par