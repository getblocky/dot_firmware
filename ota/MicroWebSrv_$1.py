 c) for c in s)

	def _tryAllocByteArray(size) :
		for x in range(10) :
			try :
				core.gc.collect()
				return bytearray(size)
			except :
				pass
		return None

	def _tryStartThread(func, args=()) :
		for x in range(10) :
			try :
				core.gc.collect()
				core.start_new_thread(func, args)
				return True
			except :
				pass
		return False

	def _unquote(s) :
		r = s.split('%')
		for i in range(1, len(r)) :
			s = r[i]
			try :
				r[i] = chr(int(s[:2], 16)) + s[2:]
			except :
				r[i] = '%' + s
		return ''.join(r)

	def _unquote_plus(s) :
		return MicroWebSrv._unquote(s.replace('+', ' '))

	def _fileExists(path) :
		try :
			stat(path)
			return True
		except :
			return False

	def _isPyHTMLFile(filename) :
		return filename.lower().endswith(MicroWebSrv._pyhtmlPagesExt)
	
	# ===( Constructor )==========================================================
	
	def __init__( self,
					routeHandlers = None,
					port			= 80,
					bindIP		= '0.0.0.0',
					webPath		 = "/flash/www" ) :
