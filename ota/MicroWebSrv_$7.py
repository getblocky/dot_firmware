f._method	= elements[0].upper()
					self._path	= elements[1]
					self._httpVer = elements[2].upper()
					elements		= self._path.split('?', 1)
					if len(elements) > 0 :
						self._resPath = MicroWebSrv._unquote_plus(elements[0])
						if len(elements) > 1 :
							self._queryString = elements[1]
							elements = self._queryString.split('&')
							for s in elements :
								param = s.split('=', 1)
								if len(param) > 0 :
									value = MicroWebSrv._unquote(param[1]) if len(param) > 1 else ''
									self._queryParams[MicroWebSrv._unquote(param[0])] = value
					return True
			except :
				pass
			return False
	
		
		def _parseHeader(self, response) :
			while True :
				elements = self._socket.readline().decode().strip().split(':', 1)
				if len(elements) == 2 :
					self._headers[elements[0].strip()] = elements[1].strip()
				elif len(elements) == 1 and len(elements[0]) == 0 :
					if self._method == 'POST' :
						self._contentType	 = self._headers.get("Content-Type", N