async def waitReady(self,timeout = 1000):
		while self.running == True:
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
		self.running = False
		print(r)
		return r
		
		
	async def request(self,cmd,prefix = None,timeout = 1000):
		# Make sure the module is ready
		
		print('\t[SIM800] Request',cmd,end='')
		if prefix == None :
			prefix = ''
			for x in range(len(cmd)):
				if cmd[x].isalpha() or cmd[x] == '+':
					prefix += cmd[x]
				else :
					break
			prefix = bytes(prefix,'utf-8')
		else :
			if isinstance(prefix,str):
				prefix = bytes(prefix,'utf-8')
			
		cmd= bytes(cmd,'utf-8') if isinstance(cmd,str) else cmd
		await self.waitReady(timeout)
		#print('Requesting [{}] [{}]'.format(cmd,prefix))
		self.write(cmd)
		if not prefix in self.waitinglist:
			self.waitinglist.append(prefix)
		while prefix in self.waitinglist:
			await asyncio.sleep_ms(1)
			#print('>',end='')
		#print('\t <<< Return [{}]'.format(self.dict[prefix]))
		self.running = False
		print("\t[SIM800] Request Done -> ",self.dict[prefix])
		return self.dict.pop(prefix)
		
	async def getSignalQuality