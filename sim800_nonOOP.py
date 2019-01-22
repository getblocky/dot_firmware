#version=1.0
#hash=1123
import sys;sys.modules['Blocky.];from micropython import const;from time import ticks_ms as tm;from time import ticks_diff as td;from time import sleep_ms as ts;from machine import UART;s=asyncio.sleep_ms;i=isinstance;p=print
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
	port=port;p=getPort(port);d=debug;s=setting;fc=F;b='';fr=F;fp=F;le={};lr=N;lc=N;a=F;ls=[N for _ in range(6)]
	if ext_socket==None  or not ext_socket.isconnected():
		ext=eeprom.get('EXT_SOCKET')
		if ext !=T:
			eeprom.set('EXT_SOCKET',T);machine.reset()
		if hardware['uart'].count(None)==0:
			raise Exception('no uart')
		i=hardware['uart'].index(None);u=UART(i,rx=p[0],tx=p[1]);hardware['uart'][i]=self
		while True:
			u.write('AT\r\n');ts(100)
			if u.any()>0:
				a=u.read()
				if a.count('OK'):
					break
		ext_socket=self
		mainthread.create_task(rSMS());mainthread.create_task(connect());mainthread.create_task(_routine());deinit_list.append(self)
def deinit(self):
	hardware['uart'][i]=None
def isconnected(self):
	return fc
async def _routine(self):
	while T:
		await s(100)
		if fp==F and u.any():
			while u.any()>0:
				b +=u.read()
			j()
async def r(self,d,w=N,to=5000):
	d=b(d);w=b(w)
	while fr==T:
		await s(10)
	fr=T
	if w==N:
		w=''
		for x in range(len(d)):
			if d[x:x+1] in [' ','+',','] or d[x:x+1].isalpha() or d[x:x+1].isdigit():
				w +=d[x:x+1]
	elif i(w,str)or i(w,bytearray):
		w=b(w)
	lr=w;st=tm();await write(('AT' if d.startswith('+') else '')+d+('\r\n' if d.startswith('+') else ''));fp=T
	while lr==w:
		j()
		if u.any()==0 and len(b):
			j()
		if u.any()>0:
			b +=u.read()
		if td(tm(),st)>to:
			fr=F;fp=F;raise OSError
	fr=F;fp=F;return lr
async def w(self,d,to=60000):
	d=b(d);le[d]=N;st=tm()
	while le[d]==N:
		await s(50)
		if td(tm(),st)>to:
			le.pop(d);raise OSError
	return le.pop(d)
async def c(self,d,r=['OK','ERROR'],to=10000):
	while fr==T:
		await s(50)
	fr=T;d=b(d);lc=r
	for x in range(len(lc)):
		lc[x]=b(lc[x])
	if u.any()>0:
		b+=u.read();j()
	await write(('AT' if d.startswith('+') else '')+d+('\r\n' if d.startswith('+') else ''))
	fp=T;st=tm()
	while not i(lc,int):
		if u.any()==0:
			await s(50)
			if td(tm(),st)>to:
				fr=F;fp=F;raise OSError
		if u.any()>0:
			b +=u.read();j()
	fp=F;fr=F;return lc
async def write(self,d):
	if u.any()>0:
		b +=u.read()
	if len(b):
		j()
	else:
		u.write(d)
def j (self):
	while len(b)>0:
		if b.count('\r') + b.count('\n')==0:
			t=b;b=''
		elif len(b) <=2 and len(b.strip())==0:
			b='';return
		else:
			start=max((b.find('\r'),b.find('\n')));stop=max((b.find('\r',1),b.find('\n',1)))
			if start==0:
				if stop==-1:
					t=b;b=''
				else:
					t=b[1:stop];b=b[stop:]
			else:
				t=b[:stop];b=b[stop:]

		t=t.lstrip();a=F;je(t);jc(t);jr(t)
def je(self,d):
	if a:
		return
	for key in le.keys():
		if d.find(key)>-1:
			a=T
			if d==key:
				le[key]=T
			else:
				if d.find(': ')>-1:
					d=d.split(': ')[1].split(',')
					for x in range(len(d)):
						try:
							d[x]=int(d[x])
						except ValueError:
							pass
					le[key]=d
			return
def jc(self,d):
	if a:
		return
	if i(lc,list) and d in lc:
		lc=lc.index(d);a=T
def jr(self,d):
	if a:
		return
	if lr==N:
		return
	elif i(lr,bytes) and lr.startswith('*'):
		if lr=='*':
			lr=[d]
		else:
			lr=lr[1:]
		a=T
	elif i(lr,bytes) and not lr.startswith('*'):
		if d.startswith(lr):
			d=d[len(lr):];d=d.split(':')[-1].split(',')
			for x in range(len(d)):
				try:
					d[x]=int(d[x])
				except ValueError:
					pass
			a=T;lr=d
	elif i(lr,int):
		length=lr
		while len(d) + len(b) < length:
			if u.any()>0:
				b +=u.read();ts(10)
		lr=d[0:min(len(d),lr)]
		if len(lr) < length:
			missing=length - len(lr);lr +=b[0:missing];b=b[missing:]
async def connect (self):
	u.write('ATE0\r\n');u.read();r=await r('+CFUN?')
	if r[0] !=1:
		r=await c('+CFUN=1')
		if r !=0:
			return F
	r=await r('+CGATT?')
	if r[0] !=1:
		while True:
			r=await c('+CGATT=1')
			if r==0:
				break
	await c('+SAPBR=3,1,"Contype","GPRS"');await c('+SAPBR=3,1,"APN","{}"'.format(s['apn']));await c('+SAPBR=3,1,"USER","{}"'.format(s['user']));await c('+SAPBR=3,1,"PWD","{}"'.format(s['pwd']));await c('+CGDCONT=1,"IP","{}"'.format(s['apn']));await c('+CGACT=1,1',to=10000);await c('+SAPBR=1,1',to=5000);await r('+SAPBR=2,1',w='+SAPBR:',to=5000);await c('+CGATT=1');await c('+CIPMUX=1');await c('+CIPQSEND=1');await c('+CIPRXGET=1');await c('+CSTT="{}"'.format(s['apn']));await c('+CIICR');await r('+CIFSR',w='*');await c('+CDNSCFG="{}"'.format(s['dns']));fc=T
def socket(self,af=2,type=1,proto=6 ):
	class socket:
	def __init__(self,super,mode=0):
			s=super;id=s.ls.index(N);s.ls[id]=self;sockMode=mode;to=0;b='';fc=F
async def settimeout(self,timeout):
			return
async def setto (self,to):
			return
async def close(self):
			r=await s.c('+CIPCLOSE={},0'.format(id),r=[bytes(str(id),'utf-8') + ', ' + x for x in ['CLOSE OK','ERROR']])
			if r==0:
				s.ls[id]=N;fc=F
			return r==0
async def connect(self,addr):
			while s.fc==F:
				await s(1000)
			await s.c('+CIICR');await s.r('+CIFSR',w='*');r=await s.c('+CIPSTART={},"{}","{}",{}'.format(id,"UDP" if sockMode==s.SOCK_DGRAM else "TCP",addr[0],addr[1]),r=[bytes(str(id),'utf-8') + ', ' + x for x in ['CONNECT OK','ALREADY CONNECT','CONNECT FAIL'] ],to=15000)
			if r !=2:
				fc=T
			return F if r==2 else T
async def recv(self,length,to=5000):
			while not fc:
				await s(300)
			try:
				a=await s.r('+CIPRXGET=4,{}'.format(id),w='+CIPRXGET: 4,{id},'.format(id=id))
				if a[0]==0:
					await s.w('+CIPRXGET: 1,{}'.format(id));a=await s.r('+CIPRXGET=4,{}'.format(id),w='+CIPRXGET: 4,{id},'.format(id=id))
				a=a[0]
				if a < length:
					return ''
				l=18+len(str(length)+str(a-length)) + length;d=await s.r('+CIPRXGET=2,{},{}'.format(id,length),w=l);d=d[-length:];return d
			except OSError:
				raise OSError(errno.EAGAIN)
async def sendto(self,d,addr):
			await connect(addr);await write(d)
async def send (self,d,length=N):
			await write(d,length)
async def write(self,d,length=N):
			await s.c('+CIPSEND={},{}'.format(id,length or len(d)),r=['> ']);d=b(d);await s.r(d,w='DATA ACCEPT:{},'.format(id))
	_socket_=socket(self,type)
	return _socket_
async def sendSMS(self,number,content):
	await c('+CMGF=1')
	await c('+CSCS="GSM"')
	await c('+CMGS="{}"'.format(number),r=['> '])
	m=bytes(content,'utf-8')+'\x1a'
	u.write(m)
async def rSMS(self):
	while True:
		try:
			await s(100)
		except OSError:
			pass
			#a = \'\xc1 H\xed H\xed\'

async def readSMS(self,i):
	r = await r('+CMGR={}'.format(i),w='+CMGR: ')
	return r
def whenReceiveSMS(self,function):
	_fsms = function
def deinit(self):
	eeprom.set('EXT_SOCKET',False);hardware['uart'][i]=N
