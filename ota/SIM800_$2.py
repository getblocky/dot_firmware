(self):
		r = await self.request('+CSQ')
		return r
			
		
	async def routine(self):
		# In harmonic with command and request
		self.buf = b''
		while True :
			await asyncio.sleep_ms(5)
			if self.uart.any() == 0 and len(self.buf) > 0:
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
					
				print('\t\t[SIM800] Receive ',self.buf)
				print('\t\t\tCommand =  ',cmd)
				print('\t\t\tAnswer =  ',ans)
				print('\t\t\tData =  ',data)
				
				
				#print('<raw>',cmd,ans,resp,data)
				if isinstance(self.responselist,list) and cmd in self.responselist:
					self.responselist = self.responselist.index(cmd)
					#print('<recv> Reponse = {}'.format(self.responselist))
				elif cmd in self.waitinglist:
					if cmd in self.waitinglist : # Damn you CIFSR
						self.waitinglist.remove(cmd)
						self.dict[cmd] = ans
						if len(data):
							data = data[0:-5]
							self.dict[cmd].append(data)
					else :
						print('No prefix' , self.echo, cmd)
				else :
					prefix = self.echo[2:-3]
					if prefix in self.waitinglist:
						self.waitinglist.remove(prefix)
					self.dict[prefix] = cmd
					#print('<recv> Request = {}'.format(self.dict[cmd]))
				self.buf = b''
				
			if self.uart.any() > 0:
				self.buf = self.uart.read()
	async def sendSMS(self,number,message):
		#print('Sending SMS to ', number)
		await self.command('+CMGF=1')
		await self.command('+CSCS="GSM"')
		await self.command('+CMGS="{}"'.format(number