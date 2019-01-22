ator.show('blynk-authenticating')
				self.state = AUTHENTICATING
				hdr = core.struct.pack(HDR_FMT, MSG_LOGIN, self._new_msg_id(), len(self._token))
				print('Blynk connection successful, authenticating...')
				await self._send(hdr+self._token)
				data = await self._recv(HDR_LEN,timeout = MAX_SOCK_TO)
				if not data :
					await self._close('authentication timed out')
					continue
				msg_type, msg_id, status = core.struct.unpack(HDR_FMT, data)
				if status != STA_SUCCESS or msg_id == 0:
					await self._close('authentication failed')
					continue
				await core.indicator.show('blynk-authenticated')
				self.state = AUTHENTICATED
				await self._send(self._format_msg(MSG_INTERNAL, 'ver', '0.1.3', 'buff-in', 4096, 'h-beat', HB_PERIOD, 'dev', core.sys.platform+'-py'))
				print('[Blynk] Connected ! , Happy Blynking :)')
				await core.indicator.pulse(color = (0,40,0))
				core.flag.blynk = True
				await self.log('[BLYNK] Online at {}'.format(core.Timer.current('clock')))

			if