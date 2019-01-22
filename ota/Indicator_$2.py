ancel) == True and cancel() != reverse ) or (callable(cancel) == False and cancel != reverse):
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

				colour = tuple(colour)

			start = max(1,int(start))
			stop = min(12,int(stop))
			if start > stop :
				return
			for x in range(start,stop+1):
				self.rgb[x-1] = colour
			if update == True