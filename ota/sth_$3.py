tf-8')
						elif isinstance(data,bytearray):
							data = bytes(data)
					except TypeError as error:
						import sys
						sys.print_exception(error)
						if self.debug :
							print('[ERROR] Can not convert to bytes')
							print('BUF = ',data)

				r = await self.super.request(data , prefix = b'DATA ACCEPT:{},'.format(self.id),iscmd=True)

		new_socket = socket(self , *args,**kwargs)
		return new_socket

	def trigger (self,kw,func):
		pass




	async def waitReady(self):
		return
		while self.running == True :
			await asyncio.sleep_ms(1)
		self.running = True
		self.polling = True
		while True :
			if len(self.buffer):
				self.parsing()
			await self.write(b'AT\r\n')
			await asyncio.sleep_ms(100)
			if self.uart.any() > 0:
				temp=self.uart.read();self.buffer+=temp;self.debugport.write(b'>>>'+temp)
				if self.debug :
					print('\t\t[READY]\t\t' , end = '')
				if b'OK' in self.buffer:
					self.polling = False
					self.running = False
					return
				self.parsing()



	