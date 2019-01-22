one)
						self._contentLength = int(self._headers.get("Content-Length", 0))
					return True
				else :
					return False
		
		def _getConnUpgrade(self) :
			if 'upgrade' in self._headers.get('Connection', '').lower() :
				return self._headers.get('Upgrade', '').lower()
			return None
		
		def ReadRequestContent(self, size=None) :
			self._socket.setblocking(False)
			b = None
			try :
				if not size :
					b = self._socket.read(self._contentLength)
				elif size > 0 :
					b = self._socket.read(size)
			except :
				pass
			self._socket.setblocking(True)
			return b if b else b''
		
		def ReadRequestPostedFormData(self) :
			res	= { }
			data = self.ReadRequestContent()
			if len(data) > 0 :
				elements = data.decode().split('&')
				for s in elements :
					param = s.split('=', 1)
					if len(param) > 0 :
						value = MicroWebSrv._unquote(param[1]) if len(param) > 1 else ''
						res[MicroWebSrv._unquote(param[0])] = value
			return res
		
	
	# ===( Class Response	)=============