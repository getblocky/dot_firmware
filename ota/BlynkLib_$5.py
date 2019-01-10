				core.gc.collect()
					core.indicator.show('blynk-connecting')
					self.state = CONNECTING
					
					if not self._ext_socket :
						print('TCP: Connting to {} : {}'.format(self._server,self._port))
						self.conn = core.socket.socket() 
						self.conn.settimeout(1)
					else :
						while core.ext_socket == None:
							await core.wait(500)
						self.conn = core.ext_socket.socket()
						await self.conn.settimeout(2)
					while True :
						try :
							if not self._ext_socket:
								b = core.socket.getaddrinfo(self._server,self._port)[0][4]
								self.conn.connect(b)
								break
							else :
								await self.conn.connect(self._server,self._port)
								break
						except OSError as err:
							import sys;sys.print_exception(err)
							print('>')
							await core.wait(5000)
							continue
					print('Socket: Connected at {}'.format(core.Timer.runtime()))
				except Exception as err:
					core.sys.print_exception(err)
					await self._close('connection with the Blynk servers failed')
					break
				
				await core.indicator.show('blynk-authenticating')
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
				await self.log('[BLYNK] 