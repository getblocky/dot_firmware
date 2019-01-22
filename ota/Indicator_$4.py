)
					for x in range(3):
						if target_color[i][x] != self.rgb[i][x] :
							new[x] = self.rgb[i][x]-1 if self.rgb[i][x] > target_color[i][x] else self.rgb[i][x] + 1
					self.rgb[i] = new
				self.rgb.write()
		await core.call_once('indicator',temp)




	async def show (self , state):
		if state == 'blynk-authenticating':
			@core.asyn.cancellable
			async def temp ():
				while True :
					for x in range(12):
						await core.wait( abs(6-x)*5 )
						self.rgb.fill((0,0,0))
						self.rgb[x] = (25,0,25)
						self.rgb[x-1 if x-1 >=0 else 11-x] = (10,0,10)
						self.rgb[x-2 if x-2 >=0 else 11-x] = (5,0,5)
						self.rgb.write()
			await core.call_once('indicator',temp)
		elif state == 'wifi-connecting':
			@core.asyn.cancellable
			async def temp ():
				while True :
					for x in range(12):
						await core.wait( abs(6-x)*5 )
						self.rgb.fill((0,0,0))
						self.rgb[x] = (50,25,0)
						self.rgb[x-1 if x-1 >=0 else 11-x] = (20,10,0)
						self.rgb[x-2 if x-2 >=0 else 11-x] = (