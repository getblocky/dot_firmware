self.running == True:
			await asyncio.sleep_ms(1)
		self.running = True
		
		self.responselist = [b'OK']
		self.write('')
		#print('\t',end='')
		while True :
			print('#',end='')
			await asyncio.sleep_ms(50)
			
			for _ in range(10):
				if isinstance(self.responselist,list) and b'OK' in self.responselist:
					await asyncio.sleep_ms(10)
				else :
					break
			if isinstance(self.responselist,list) and b'OK' in self.responselist:
				self.write('')
			else :
				#print('\t<ready>')
				break
				
		
			
				
		
		
	async def command(self,cmd,prefix=['OK','ERROR'],timeout=1000):
		print('\t[SIM800] Command' , cmd , end = '')
		# Make sure the module is ready
		await self.waitReady(timeout)
		self.responselist = []
		for x in range(len(prefix)):
			self.responselist.append(bytes(prefix[x],'utf-8') if isinstance(prefix[x],str) else prefix[x])
		
		self.write(cmd)
		while isinstance(self.responselist,list):
			await asyncio.sleep_ms(1)
		
		
		r = self.responselist
		self.running = Fa