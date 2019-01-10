lable(cancel) == True and cancel() != reverse ) or (callable(cancel) == False and cancel != reverse):
					break
				
				for x in range(12):
					await core.wait(gap)
					self.rgb.fill((0,0,0))
					for i in range(12) :
						self.rgb.fill((0,0,0))
						for fade in range(1,12):
							self.rgb[i-fade if x-fade >= 0 else 11-fade] = (color//fade,color//fade,color//fade)
							self.rgb[i] = color
							self.rgb[x-1 if x-1 >=0 else 11-x] = (color//2,color//2,color)
							self.rgb[x-2 if x-2 >=0 else 11-x] = (5,0,5)
							self.rgb.write()
							# do something here 
		await core.call_once('indicator',temp)
		
	def colour (self,start,stop,colour,update=True):
		try :
			if isinstance(colour,str):
				colour = colour.lstrip('#')
				colour = list(max(0,min(255,int(colour[i:i+2], 16))) for i in (0, 2 ,4))
				
				for x in range(3):
					colour[x] = colour[x] // 10
				colour = tuple(colour)
				
			start = max(1,int(start))
			stop = min(12,int(stop))
			if start > stop :
				return
			for x in range(start,stop+1):
				self.rgb[x-1] = colour
			if update == True :
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
