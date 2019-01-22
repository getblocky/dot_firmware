onselist:
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
		await self.command('+CMGS="{}"'.format(number),prefix=['>'])
		#print('Message = ',message)
		self.uart.write(message)
		self.uart.write(bytearray([0x1A]))
		#pri