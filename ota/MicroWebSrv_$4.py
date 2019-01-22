tarted(self) :
		return self._started

	def SetNotFoundPageUrl(self, url=None) :
		self._notFoundUrl = url

	def GetMimeTypeFromFilename(self, filename) :
		filename = filename.lower()
		for ext in self._mimeTypes :
			if filename.endswith(ext) :
				return self._mimeTypes[ext]
		return None

	def GetRouteHandler(self, resUrl, method) :
		if self._routeHandlers :
			resUrl = resUrl.upper()
			method = method.upper()
			for route in self._routeHandlers :
				if len(route) == 3 and			\
					 route[0].upper() == resUrl and \
					 route[1].upper() == method :
					 return route[2]
		return None

	def _physPathFromURLPath(self, urlPath) :
		if urlPath == '/' :
			for idxPage in self._indexPages :
				physPath = self._webPath + '/' + idxPage
				if MicroWebSrv._fileExists(physPath) :
					return physPath
		else :
			physPath = self._webPath + urlPath
			if MicroWebSrv._fileExists(physPath) :
				return physPath
		return None
	
	# ===( Class Client	)==========================================