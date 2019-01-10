self._new_msg_id(), len(self._token))
				print('Blynk connection successful, authenticating...')
				await self._send(hdr+self._token)
				data = await self._recv(HDR_LEN,timeout = MAX_SOCK_TO)
				if not data :
					await self._close('authentication timed out')
					continue
				msg_type, msg_id, status = struct.unpack(HDR_FMT, data)
				print('[Blynk] Msg : Type = {} , Id = {} , Status = {} , Raw = {}'.format(msg_type,msg_id,status,data))
				if status != STA_SUCCESS or msg_id == 0:
					await self._close('authentication failed')
					continue
				self.state = AUTHENTICATED
				import sys
				await self._send(self._format_msg(MSG_INTERNAL, 'ver', '0.1.3', 'buff-in', 4096, 'h-beat', HB_PERIOD, 'dev', sys.platform+'-py'))
				print('[Blynk] Connected ! , Happy Blynking :)')
				blynk = True
				await self.log('[BLYNK] Online at {}'.format(ticks_ms()))
				
			if self.state == AUTHENTICATED:
				break
		# connection established , perform polling
		self._hb_time = 0
		self._last_hb_id = 0
		self._tx_count = 0
		blynk = True
		while True :
			self.last_call = ticks_ms()
			try :
				data = await self._recv(HDR_LEN,NON_BLK_SOCK)
			except:
				pass
			if data:
				msg_type,msg_id,msg_len = struct.unpack(HDR_FMT,data)
				if msg_id == 0:
					await self._close('invalid msg id : {}'.format(msg_len))
					break
				if msg_type == MSG_RSP:
					if msg_id == self._last_hb_id:
						self._last_hb_id = 0
				elif msg_type == MSG_PING:
					await self._send(struct.pack(HDR_FMT,MSG_RSP,msg_id,STA_SUCCESS))
				elif msg_type == MSG_HW or msg_type == MSG_BRIDGE:
					data = await self._recv(msg_len,MIN_SOCK_TO)
					if data :
						await self._handle_hw(data)
				else :
					print('close: unknown message type {} , ignoring'.format(msg_type))
					continue
			else :
				await asyncio.sleep_ms(1)
				
			if not self._server_alive():
				await self._close('blynk server is offline')
				print('[Blynk] Connecting back to server')
				blynk = False
				return
			else :
				blynk = True