=========================================
	
	class _response :
		
		def __init__(self, client) :
			self._client = client
		
		def _write(self, data) :
			try :
				
				if isinstance(data , str) or isinstance(data , bytes):
					print('socket_write' , data , len(data))
					return self._client._socket.write(data)
				elif isinstance(data , list):
					for x in data :
						self._client._socket.write(x)
					
				
			except Exception as err:
				print('socket->_write->' , err)
		
		def _writeFirstLine(self, code) :
			reason = self._responseCodes.get(code, ('Unknown reason', ))[0]
			self._write("HTTP/1.0 %s %s\r\n" % (code, reason))
		
		def _writeHeader(self, name, value) :
			self._write("%s: %s\r\n" % (name, value))
		
		# delete
		def _writeContentTypeHeader(self, contentType, charset=None) :
			if contentType :
				ct = contentType \
					 + (("; charset=%s" % charset) if charset else "")
			else :
				ct = "application/octet-stream"
			self._writeHeader("Content-Type", ct)
		
		