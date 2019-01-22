 :
				self.rgb.write()
		except :
			pass
	async def pulse ( self , color , speed=10,gap = 1):
		@core.asyn.cancellable
		async def temp ():
			while color != self.rgb[0]:
				self.rgb.fill( ( min(color[0],self.rgb[0][0]+gap),min(color[1],self.rgb[0][1]+gap) ,min(color[2],self.rgb[0][2]+gap)  ) )
				self.rgb.write()
				await core.wait(speed)
			while (0,0,0) != self.rgb[0]:
				self.rgb.fill( ( max(0,self.rgb[0][0]-gap),max(0,self.rgb[0][1]-gap) ,max(0,self.rgb[0][2]-gap)  ) )
				self.rgb.write()
				await core.wait(speed)
		await core.call_once('indicator',temp)
	async def rainbow ( self , speed = 10):
		@core.asyn.cancellable
		async def temp():
			target_color = list(self.rgb)
			option = [(10,0,0),(0,10,0),(0,0,10),(0,0,0)]
			for i in range(12) :
				target_color[i] = core.random.choice(option)
			while True :
				await core.wait(speed)
				for i in range(12):
					if self.rgb[i] == target_color[i]:
						target_color[i] = core.random.choice(option)
					new = list(self.rgb[i]