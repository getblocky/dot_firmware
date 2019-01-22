riteResponseMethodNotAllowed()
						elif upg == 'websocket' and 'MicroWebSocket' in globals() \
							 and self._microWebSrv.AcceptWebSocketCallback :
								MicroWebSocket( socket		 = self._socket,
												httpClient	 = self,
												httpResponse	 = response,
												maxRecvLen	 = self._microWebSrv.MaxWebSocketRecvLen,
												threaded		 = self._microWebSrv.WebSocketThreaded,
												acceptCallback = self._microWebSrv.AcceptWebSocketCallback )
								return
						else :
							response.WriteResponseNotImplemented()
					else :
						response.WriteResponseBadRequest()
			except Exception as err:
				core.sys.print_exception(err)
				#response.WriteResponseInternalServerError()
			try :
				print('Socket Close')
				self._socket.close()
			except Exception as err:
				import sys; sys.print_exception(err)
				pass
		
		def _parseFirstLine(self, response) :
			try :
				elements = self._socket.readline().decode().strip().split()
				if len(elements) == 3 :
					sel