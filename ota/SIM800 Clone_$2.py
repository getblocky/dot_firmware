lse
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
		
	async def getSignalQuality(self):
		r = await self.request('+CSQ')
		return 