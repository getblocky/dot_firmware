==============
	
	class _client :
		
		def __init__(self, microWebSrv, socket, addr) :
			socket.settimeout(2)
			self._microWebSrv	 = microWebSrv
			self._socket		= socket
			self._addr			= addr
			self._method		= None
			self._path			= None
			self._httpVer		 = None
			self._resPath		 = "/"
			self._queryString	 = ""
			self._queryParams	 = { }
			self._headers		 = { }
			self._contentType	 = None
			self._contentLength = 0
			#await self._processRequest()
		
		def _processRequest(self) :
			try :
				response = MicroWebSrv._response(self)
				if self._parseFirstLine(response) :
					if self._parseHeader(response) :
						upg = self._getConnUpgrade()
						if not upg :
							routeHandler = self._microWebSrv.GetRouteHandler(self._resPath, self._method)
							if routeHandler :
								#routeHandler(self, response)
								#loop = asyncio.get_event_loop()
								#loop.create_task(routeHandler(self,response))
								routeHandler(self,response)
							
							else :
								response.W