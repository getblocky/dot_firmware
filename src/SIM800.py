#version=1.0
#hash=1123
import sys;core=sys.modules['Blocky.Core'];from micropython import const;from time import ticks_ms as tm;from time import ticks_diff as td;from time import sleep_ms as ts;from machine import UART;s=core.asyncio.sleep_ms;i=isinstance;p=print
F=False;T=True;N=None
def b (d):
	if i(d,bytearray):
		return bytes(d)
	elif i(d,str):
		return bytes(d,'utf-8')
	elif i(d,bytes) or i(d,int):
		return d
class SIM800:
	def __init__(self,port,setting,gprs=F,debug=F):
		self.port=port;self.p=core.getPort(self.port);self.d=debug;self.s=setting;self.fc=F;self.b=b'';self.fr=F;self.fp=F;self.le={};self.lr=N;self.lc=N;self.a=F;self.ls=[N for _ in range(6)]
		self.AF_INET=2;self.AF_INET6=10;self.IPPROTO_IP=0;self.IPPROTO_TCP=6;self.IPPROTO_UDP=17;self.IP_ADD_MEMBERSHIP=3;self.SOCK_DGRAM=2;self.SOCK_RAW=3;self.SOCK_STREAM=1;self.SOL_SOCKET=4095;self.SO_REUSEADDR=4;self.fc=F
		if core.ext_socket==None  or not core.ext_socket.isconnected():
			ext=core.eeprom.get('EXT_SOCKET')
			if ext !=T:
				core.eeprom.set('EXT_SOCKET',T);core.machine.reset()
			if core.hardware['uart'].count(None)==0:
				raise Exception('no uart')
			self.i=core.hardware['uart'].index(None);self.u=UART(self.i,rx=self.p[0],tx=self.p[1]);core.hardware['uart'][self.i]=self
			while True:
				self.u.write('AT\r\n');ts(100)
				if self.u.any() > 0:
					a=self.u.read()
					if a.count(b'OK'):
						break
			core.ext_socket=self
			core.mainthread.create_task(self.rSMS());core.mainthread.create_task(self.connect());core.mainthread.create_task(self._routine());core.deinit_list.append(self)
	def deinit(self):
		core.hardware['uart'][self.i]=None
	def isconnected(self):
		return self.fc
	async def _routine(self):
		while T:
			await s(100)
			if self.fp==F and self.u.any():
				while self.u.any() > 0:
					self.b +=self.u.read()
				self.j()
	async def r(self,d,w=N,to=5000):
		d=b(d);w=b(w)
		while self.fr==T:
			await s(10)
		self.fr=T
		if w==N:
			w=b''
			for x in range(len(d)):
				if d[x:x+1] in [b' ',b'+',b','] or d[x:x+1].isalpha() or d[x:x+1].isdigit():
					w +=d[x:x+1]
		elif i(w,str)or i(w,bytearray):
			w=b(w)
		self.lr=w;st=tm();await self.write((b'AT' if d.startswith(b'+') else b'')+d+(b'\r\n' if d.startswith(b'+') else b''));self.fp=T
		while self.lr==w:
			self.j()
			if self.u.any()==0 and len(self.b):
				self.j()
			if self.u.any() > 0:
				self.b +=self.u.read()
			if td(tm(),st)>to:
				self.fr=F;self.fp=F;raise OSError
		self.fr=F;self.fp=F;return self.lr
	async def w(self,d,to=60000):
		d=b(d);self.le[d]=N;st=tm()
		while self.le[d]==N:
			await s(50)
			if td(tm(),st) > to:
				self.le.pop(d);raise OSError
		return self.le.pop(d)
	async def c(self,d,r=[b'OK',b'ERROR'],to=10000):
		while self.fr==T:
			await s(50)
		self.fr=T;d=b(d);self.lc=r
		for x in range(len(self.lc)):
			self.lc[x]=b(self.lc[x])
		if self.u.any()>0:
			self.b+=self.u.read();self.j()
		await self.write((b'AT' if d.startswith(b'+') else b'')+d+(b'\r\n' if d.startswith(b'+') else b''))
		self.fp=T;st=tm()
		while not i(self.lc,int):
			if self.u.any()==0:
				await s(50)
				if td(tm(),st) > to:
					self.fr=F;self.fp=F;raise OSError
			if self.u.any() > 0:
				self.b +=self.u.read();self.j()
		self.fp=F;self.fr=F;return self.lc
	async def write(self,d):
		if self.u.any() > 0:
			self.b +=self.u.read()
		if len(self.b):
			self.j()
		else:
			self.u.write(d)
	def j (self):
		while len(self.b) > 0:
			if self.b.count(b'\r') + self.b.count(b'\n')==0:
				t=self.b;self.b=b''
			elif len(self.b) <=2 and len(self.b.strip())==0:
				self.b=b'';return
			else:
				start=max((self.b.find(b'\r'),self.b.find(b'\n')));stop=max((self.b.find(b'\r',1),self.b.find(b'\n',1)))
				if start==0:
					if stop==-1:
						t=self.b;self.b=b''
					else:
						t=self.b[1:stop];self.b=self.b[stop:]
				else:
					t=self.b[:stop];self.b=self.b[stop:]

			t=t.lstrip();self.a=F;self.je(t);self.jc(t);self.jr(t)
	def je(self,d):
		if self.a:
			return
		for key in self.le.keys():
			if d.find(key) > -1:
				self.a=T
				if d==key:
					self.le[key]=T
				else:
					if d.find(b': ') > -1:
						d=d.split(b': ')[1].split(b',')
						for x in range(len(d)):
							try:
								d[x]=int(d[x])
							except ValueError:
								pass
						self.le[key]=d
				return
	def jc(self,d):
		if self.a:
			return
		if i(self.lc,list) and d in self.lc:
			self.lc=self.lc.index(d);self.a=T
	def jr(self,d):
		if self.a:
			return
		if self.lr==N:
			return
		elif i(self.lr,bytes) and self.lr.startswith(b'*'):
			if self.lr==b'*':
				self.lr=[d]
			else:
				self.lr=self.lr[1:]
			self.a=T
		elif i(self.lr,bytes) and not self.lr.startswith(b'*'):
			if d.startswith(self.lr):
				d=d[len(self.lr):];d=d.split(b':')[-1].split(b',')
				for x in range(len(d)):
					try:
						d[x]=int(d[x])
					except ValueError:
						pass
				self.a=T;self.lr=d
		elif i(self.lr,int):
			length=self.lr
			while len(d) + len(self.b) < length:
				if self.u.any() > 0:
					self.b +=self.u.read();ts(10)
			self.lr=d[0:min(len(d),self.lr)]
			if len(self.lr) < length:
				missing=length - len(self.lr);self.lr +=self.b[0:missing];self.b=self.b[missing:]
	async def connect (self):
		self.u.write('ATE0\r\n');self.u.read();r=await self.r('+CFUN?')
		if r[0] !=1:
			r=await self.c('+CFUN=1')
			if r !=0:
				return F
		r=await self.r('+CGATT?')
		if r[0] !=1:
			while True:
				r=await self.c('+CGATT=1')
				if r==0:
					break
		await self.c('+SAPBR=3,1,"Contype","GPRS"');await self.c('+SAPBR=3,1,"APN","{}"'.format(self.s['apn']));await self.c('+SAPBR=3,1,"USER","{}"'.format(self.s['user']));await self.c('+SAPBR=3,1,"PWD","{}"'.format(self.s['pwd']));await self.c('+CGDCONT=1,"IP","{}"'.format(self.s['apn']));await self.c('+CGACT=1,1',to=10000);await self.c('+SAPBR=1,1',to=5000);await self.r('+SAPBR=2,1',w=b'+SAPBR:',to=5000);await self.c('+CGATT=1');await self.c('+CIPMUX=1');await self.c('+CIPQSEND=1');await self.c('+CIPRXGET=1');await self.c('+CSTT="{}"'.format(self.s['apn']));await self.c('+CIICR');await self.r('+CIFSR',w=b'*');await self.c('+CDNSCFG="{}"'.format(self.s['dns']));self.fc=T
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
				if r !=2:
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
		_socket_=socket(self,type)
		return _socket_
	async def sendSMS(self,number,content):
		await self.c('+CMGF=1')
		await self.c('+CSCS="GSM"')
		await self.c('+CMGS="{}"'.format(number),r=[b'> '])
		m=bytes(content,'utf-8')+b'\x1a'
		self.u.write(m)
	async def rSMS(self):
		while True:
			try:
				await s(100)
			except OSError:
				pass
				#a = \'\xc1 H\xed H\xed\'

	async def readSMS(self,i):
		r = await self.r('+CMGR={}'.format(i),w='+CMGR: ')
		return r
	def whenReceiveSMS(self,function):
		self._fsms = function
	def deinit(self):
		core.eeprom.set('EXT_SOCKET',False);core.hardware['uart'][self.i]=N
