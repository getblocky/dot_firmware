XGET: 1,{id}'.format(id=self.id))
				r = await self.super.request('+CIPRXGET=2,{id},{length}'.format(id=self.id,length=length),	prefix = b'**')
				# r = [RECEIVED,PENDING]
				if r[0] == length:
					return #TODO ERROR HERE
				return r

			async def listen(self):
				pass

			async def read(self):
				pass

			async def readinto(self):
				pass

			async def readline(self):
				pass


			async def recvfrom(self):
				pass

			async def send(self):
				pass

			async def sendall(self):
				pass


			async def setblocking(self):
				pass

			async def setsockopt(self):
				pass
			async def sendto(self,data,addr):
				await self.connect( addr)
				await self.write( data )

			async def write(self , data , length = None):
				r = await self.super.command('+CIPSEND={id},{length}'.format(id = self.id , length = len(data) if length == None else data[:length]),\
					response = [b'> '])
				if not isinstance(data,bytes):
					try :
						if isinstance(data,str):
							data = bytes(data,'u