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
			if d.find(key) 