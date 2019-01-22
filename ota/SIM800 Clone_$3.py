r
			
		
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