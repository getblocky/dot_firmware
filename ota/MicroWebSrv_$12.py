arset=None, content=None) :
			return self.WriteResponse(200, headers, contentType, contentCharset, content)
		


		def WriteResponseError(self, code) :
			responseCode = self._responseCodes.get(code, ('Unknown reason', ''))
			return self.WriteResponse( code,
										 None,
										 "text/html",
										 "UTF-8",
										 self._errCtnTmpl % {
											'code'	: code,
											'reason'	: responseCode[0],
											'message' : responseCode[1]
										 } )
		
		def WriteResponseJSONError(self, code, obj=None) :
			return self.WriteResponse( code,
										 None,
										 "application/json",
										 "UTF-8",
										 dumps(obj if obj else { }) )
		
		def WriteResponseBadRequest(self) :
			return self.WriteResponseError(400)
		
		def WriteResponseForbidden(self) :
			return self.WriteResponseError(403)
		
		def WriteResponseNotFound(self) :
			if self._client._microWebSrv._notFoundUrl :
				self.WriteResponseRedirect(self._client._microWebSrv._notFoundUrl)
			else :
	