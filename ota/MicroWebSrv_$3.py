int_exception(err)
				if self.success == True :
					print('setup success , resetting')
					break
			self._started = False
			print('CLOSE AP')
		except Exception as err:
			print( ' _socket -> ' , err)
	
	# ===( Functions )============================================================
	def setup_success(self):
		self.success = True
	async def Start(self, threaded=True) :
		if not self._started :
			reset_timer = core.machine.Timer(1)
			reset_timer.init(mode=core.machine.Timer.ONE_SHOT,period = 1800000,callback =lambda t:core.machine.reset())
			self._socket = core.socket.socket( core.socket.AF_INET,
											core.socket.SOCK_STREAM,
											core.socket.IPPROTO_TCP )
			self._socket.setsockopt( core.socket.SOL_SOCKET,
									 core.socket.SO_REUSEADDR,
									 1 )
									 
			self._socket.bind(self._srvAddr)
			self._socket.listen(1)
			self._socket.setblocking(False)
			await self._socketProcess ()
			
	def Stop(self) :
		if self._started :
			self._socket.close()

	def IsS