it self.r('+CIFSR',w=b'*');await self.c('+CDNSCFG="{}"'.format(self.s['dns']));self.fc=T
	def socket(self,af=2,type=1,proto=6 ):
		class socket:
			def __init__(self,super,mode=0):
				self.s=super;self.id=self.s.ls.index(N);self.s.ls[self.id]=self;self.sockMode=mode;self.to=0;self.b=b'';self.fc=F
			async def settimeout(self,timeout):
				return
			async def setto (self,to):
				return
			async def close(self):
				r=await self.s.c('+CIPCLOSE={},0'.format(self.id),r=[bytes(str(self.id),'utf-8') + b', ' + x for x in [b'CLOSE OK',b'ERROR']])
				if r==0:
					self.s.ls[self.id]=N;self.fc=F
				return r==0
			async def connect(self,addr):
				while self.s.fc==F:
					await s(1000)
				await self.s.c('+CIICR');await self.s.r('+CIFSR',w=b'*');r=await self.s.c('+CIPSTART={},"{}","{}",{}'.format(self.id,"UDP" if self.sockMode==self.s.SOCK_DGRAM else "TCP",addr[0],addr[1]),r=[bytes(str(self.id),'utf-8') + b', ' + x for x in [b'CONNECT OK',b'ALREADY CONNECT',b'CONNECT FAIL'] ],to=15000)
				if