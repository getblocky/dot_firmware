 [b' ',b'+',b','] or d[x:x+1].isalpha() or d[x:x+1].isdigit():
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
		