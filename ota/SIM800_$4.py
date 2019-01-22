> -1:
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
			self.lr=d[0: