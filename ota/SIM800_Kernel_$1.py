f
				
				
				self.sockMode= mode # 2 if UDP , 0 if TCP
				
				
				
			async def close(self):
				r = await self.super.command('+CIPCLOSE={},0'.format(self.id),\
					respone = [bytes(str(self.id),'utf-8') + b', ' + \
					x for x in [b'CLOSE OK',b'ERROR']]\
				);return r==0
				
			async def connect(self):
				r = await self.super.command(\
					'+CIPSTART={id},"{mode}","{addr}",{port}'.format(\
						id = self.id,\
						mode = "UDP" if self.sockMode == 2 else "TCP",\
						addr = data[0],\
						port = data[1]), \
					response = [bytes(str(self.id),'utf-8') + b', ' + x for x in [b'CONNECT OK',b'ALREADY CONNECT',b'CONNECT FAIL'] ]\
				);return False if r == 2 else True
			async def recv(self,length):
				r = await self.super.request(\
					'+CIPRXGET=2,{id},{length}'.format(id=sellf.id,length=;length),\
					#prefix = b'+CIPRXGET: 2,{id}'.format(id=self.id)\
					prefix = b'*'\ # take the next parsing
				)
				# r = [RECEIVED,PENDING]
				if r[0] == length:
					return #TODO ERROR HERE
			
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
			
			async def sendto(self):
				pass
				
			async def setblocking(self):
				pass
			
			async def setsockopt(self):
				pass
			
			async def write(self , data , len = None):
				r = await self.command('+CIPSEND={id},{length}'.format(id = self.id , length = len(data) if len == None else data[:len]),\
					response = [b'> '])
				if not isinstance(data,bytes):
					try :
						data = bytes(data,'utf-8')
					except TypeError as error:
						import sys
						sys.print_exception(error)
						print('[ERROR] Can not convert to bytes')
						print('BUF = ',data)
						
				r = await self.super.request(data , prefix = b'DATA ACCEPT:1,')
			
		new_socket = socket(self)
		return new_socket
	