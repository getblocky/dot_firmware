 r !=2:
					self.fc=T
				return F if r==2 else T
			async def recv(self,length,to=5000):
				while not self.fc:
					await s(300)
				try:
					a=await self.s.r('+CIPRXGET=4,{}'.format(self.id),w=b'+CIPRXGET: 4,{id},'.format(id=self.id))
					if a[0]==0:
						await self.s.w('+CIPRXGET: 1,{}'.format(self.id));a=await self.s.r('+CIPRXGET=4,{}'.format(self.id),w=b'+CIPRXGET: 4,{id},'.format(id=self.id))
					a=a[0]
					if a < length:
						return b''
					l=18+len(str(length)+str(a-length)) + length;d=await self.s.r('+CIPRXGET=2,{},{}'.format(self.id,length),w=l);d=d[-length:];return d
				except OSError:
					raise OSError(errno.EAGAIN)
			async def sendto(self,d,addr):
				await self.connect(addr);await self.write(d)
			async def send (self,d,length=N):
				await self.write(d,length)
			async def write(self,d,length=N):
				await self.s.c('+CIPSEND={},{}'.format(self.id,length or len(d)),r=[b'> ']);d=b(d);await self.s.r(d,w=b'DATA ACCEPT:{},'.format(self.id))
		_socket_=socket(self,