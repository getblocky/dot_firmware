Online at {}'.format(core.Timer.current('clock')))
				
			if self.state == AUTHENTICATED:
				break
		# connection established , perform polling
		self._hb_time = 0
		self._last_hb_id = 0
		self._tx_count = 0
		core.flag.blynk = True
		while True :
			self.last_call = core.Timer.runtime()
			try :
				data = await self._recv(HDR_LEN,NON_BLK_SOCK)
			except:
				pass
			if data:
				msg_type,msg_id,msg_len = core.struct.unpack(HDR_FMT,data)
				if msg_id == 0:
					await self._close('invalid msg id : {}'.format(msg_len))
					break
				if msg_type == MSG_RSP:
					if msg_id == self._last_hb_id:
						self._last_hb_id = 0
				elif msg_type == MSG_PING:
					await self._send(core.struct.pack(HDR_FMT,MSG_RSP,msg_id,STA_SUCCESS))
				elif msg_type == MSG_HW or msg_type == MSG_BRIDGE:
					data = await self._recv(msg_len,MIN_SOCK_TO)
					if data :
						await self._handle_hw(data)
				else :
					print('close: unknown message type {} , ignoring'.format(msg_type))
					continue
			else :
				await core.wait(1)
				
			if not self._server_alive():
				await self._close('blynk server is offline')
				print('[Blynk] Connecting back to server')
				core.flag.blynk = False
				await core.indicator.show('blynk-authenticating')
				return
			else :
				core.flag.blynk = True
			await core.wait(1)
		








