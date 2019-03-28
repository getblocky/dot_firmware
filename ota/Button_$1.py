		print('hold for ' , (self.his[-1] - self.his[-2] )// 1000 ,'seconds')
			self.execute('hold' ,  (self.his[-1] - self.his[-2] )// 1000 )
			self.his.clear()
	@core.asyn.cancellable
	async def _async_handler (self):
		while True :
			await core.wait(500)
			if self.button.value() == 0:
				if len(self.his) and (core.Timer.runtime() - self.his[-1]) > 500 :
					print('pressed ' , len(self.his)//2)
					core.mainthread.call_soon(self.execute('pressed' ,len(self.his)//2 ))
					self.his.clear()

	async def execute(self,type,time):
		try :
			function = self.lt.get( str(type) + str(time) )
			if function == None :
				raise Exception

			if core.flag.duplicate == False :
				await core.call_once('user_button_{}_{}_{}'.format(self.port,type,time) , function)
			else:
				core.mainthread.create_task(core.asyn.Cancellable(function)())

		except Exception as err:
			print('btn-exec->' , err)
			pass

	def deinit(self):
		self.button.irq(trigger=0)
		Pin(self.p[0],Pin.IN)
