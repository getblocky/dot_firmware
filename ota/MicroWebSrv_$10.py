def _writeEndHeader(self) :
			self._write("\r\n")
		
		#def _writeBeforeContent(self, code, headers, contentType, contentCharset, contentLength) :
		#	pass		
		
		def WriteSwitchProto(self, upgrade, headers=None) :
			self._writeFirstLine(101)
			self._writeHeader("Connection", "Upgrade")
			self._writeHeader("Upgrade",	upgrade)
			if isinstance(headers, dict) :
				for header in headers :
					self._writeHeader(header, headers[header])
		
		def WriteResponse(self, code, headers, contentType, contentCharset, content) :
			try :
				
				if isinstance(content , str) or isinstance(content , bytes):
					contentLength = len(content) if content else 0
					print('LEN ' , contentLength , contentCharset , contentType )
				elif isinstance(content , list):
					contentLength = 0
					for x in content :
						contentLength+= len(x)
				else :
					contentLength = 0
				#self._writeBeforeContent(code, headers, contentType, contentCharset, contentLength)
				
				self._writeFirstLine(code)
				