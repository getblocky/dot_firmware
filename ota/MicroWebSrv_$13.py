			return self.WriteResponseError(404)
		
		def WriteResponseMethodNotAllowed(self) :
			return self.WriteResponseError(405)
		
		def WriteResponseInternalServerError(self) :
			return self.WriteResponseError(500)
		
		def WriteResponseNotImplemented(self) :
			return self.WriteResponseError(501)
		
		_errCtnTmpl = """\
		<html>
			<head>
				<title>Error</title>
			</head>
			<body>
				<h1>%(code)d %(reason)s</h1>
				%(message)s
			</body>
		</html>
		"""
		
		_execErrCtnTmpl = """\
		<html>
			<head>
				<title>Page execution error</title>
			</head>
			<body>
				<h1>%(module)s page execution error</h1>
				%(message)s
			</body>
		</html>
		"""
		
		_responseCodes = {
			
		}




