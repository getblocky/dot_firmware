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
		return r
			
		
	async def routine(self):
		# In harmonic with command and request
		self.buf = b''
		while True :
			await asyncio.sleep_ms(5)
			if self.uart.any() == 0 and len(self.buf) > 0:
				print('\t\t\t<buf>',self.buf)
				if self.buf.startswith(self.echo):
					self.buf = self.buf[len(self.echo):]
				while self.buf.startswith(b'\r\n'):
					self.buf = self.buf[2:]
				resp = self.buf[0:self.buf.find(b'\r\n')]
				data = self.buf[self.buf.find(b'\r\n')+2:self.buf.rfind(b'\r\n\r\nOK\r')]
				# resp contains cmd and ans , see +HTTPREAD
				if resp.count(b': '):
					cmd,ans = resp.split(b': ')
				else :
					cmd = resp
					ans = b''
				ans = ans.split(b',') if ans.count(b',') else [ans]
				for x in range(len(ans)):
					try :
						ans[x] = int(ans[x]) if ans[x].count(b'.') == 0 else float(ans[x])
					except :
						pass
					
				print('\t[SIM800] Receive ',cmd,ans,data,self.buf)
				#print('<raw>',cmd,ans,resp,data)
				if isinstance(self.responselist,list) and cmd in self.resp