le
			async def temp ():
				for x in range(5):
					self.rgb.fill((0,x*8,0))
					self.rgb.write()
					await wait(10)
				for x in range(5,-1,-1):
					self.rgb.fill((0,x*8,0))
					self.rgb.write()
					await wait(10)
			await core.call_once('indicator',temp)
		elif state == 'blynk-connecting':
			@core.asyn.rgb.cancellable
			async def temp (self):
				while True :
					for x in range(255):
						self.rgb.fill((x,x,x));self.rgb.write()
						await core.wait(1)
					for x in range(255,0,-1):
						self.rgb.fill((x,x,x));self.rgb.write()
						await core.wait(1)
			await core.call_once('indicator',temp)
		if state == None :
			await core.call_once('indicator',None)
indicator = Indicator()

	





