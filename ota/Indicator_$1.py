le(exit):
				if exit() == True :
					break
			else :
				if exit == True :
					break
		self.rgb.fill(  (0,0,0) )
		self.rgb.write()


	async def animate(self , name):
		await core.asyn.rgb.NamedTask('indicator-handler').cancel ()
		if name == 'ota-success':
			@core.asyn.rgb.cancellable
			async def handler (self):
				for x in range(255):
					self.rgb.fill((x,x,x));self.rgb.write()
					await core.wait(1)
				for x in range(255,0,-1):
					self.rgb.fill((x,x,x));self.rgb.write()
					await core.wait(1)

		elif name == 'blynk-authenticating':
			pass
		elif name == 'blynk-failed':
			pass
		elif name == 'blynk-success':
			pass
		core.mainthread.create_task ( core.asyn.rgb.NamedTask('indicator-handler',self.handler) )

	async def loading(self,color,gap=10,cancel=None,reverse = False):
		# Cancel Condition either a flag or a function
		# if the confition function is reversed then set the reverse to True
		@core.asyn.cancellable
		async def temp ():
			while True :
				if (callable(c