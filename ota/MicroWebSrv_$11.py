if isinstance(headers, dict) :
					for header in headers :
						self._writeHeader(header, headers[header])
				
				if contentLength > 0 :
					#self._writeContentTypeHeader(contentType, contentCharset)
					ct = None
					
					if contentType :
						
						ct = contentType \
							 + (("; charset=%s" % contentCharset) if contentCharset else "")
						
					else :
						ct = "application/octet-stream"
					self._writeHeader("Content-Type", ct)
					self._writeHeader("Content-Length", contentLength)
				
				self._writeHeader("Server", "MicroWebSrv by JC`zic")
				self._writeHeader("Connection", "close")
				self._write("\r\n")	#self._writeEndHeader()
				
				if contentLength > 0 :
					self._write(content)
					print('_write',len(content))
				
				return True
			except MemoryError as err:
				print('mwsr->wR',err)
				return False
			except Exception as err :
				import sys
				sys.print_exception(err)
				
		

		def WriteResponseOk(self, headers=None, contentType=None, contentCh