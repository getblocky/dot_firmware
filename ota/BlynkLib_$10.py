lynk-connecting')
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
								await self.conn.connect((self._server,self._port))
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

				await core.indic