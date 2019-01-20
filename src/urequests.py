import sys ; core = sys.modules['Blocky.Core']

ext = core.eeprom.get('EXT_SOCKET')
if ext != True :
	import usocket
else :
	usocket = core.ext_socket


class Response:

	def __init__(self, f):
		self.raw = f
		self.encoding = "utf-8"
		self._cached = None

	async def close(self):
		if self.raw:
			if ext == True :
				await self.raw.close()
			else :
				self.raw.close()
			self.raw = None
		self._cached = None

	@property
	async def content(self):
		if self._cached is None:
			try:
				if ext == True :
					self._cached = await self.raw.read()
				else :
					self._cached = self.raw.read()
			finally:
				if ext == True :
					await self.raw.close()
				else :
					self.raw.close()
				self.raw = None
		return self._cached

	@property
	def text(self):
		return str(self.content, self.encoding)

	def json(self):
		import ujson
		return ujson.loads(self.content)


async def request(method, url, data=None, json=None, headers={}, stream=None):
	try:
		proto, dummy, host, path = url.split("/", 3)
	except ValueError:
		proto, dummy, host = url.split("/", 2)
		path = ""
	if proto == "http:":
		port = 80
	elif proto == "https:":
		if ext != True :
			import ussl
		port = 443
	else:
		raise ValueError("Unsupported protocol: " + proto)

	if ":" in host:
		host, port = host.split(":", 1)
		port = int(port)

	ai = usocket.getaddrinfo(host, port, 0, usocket.SOCK_STREAM)
	ai = ai[0]

	s = usocket.socket(ai[0], ai[1], ai[2])
	try:
		if ext  == True :
			await s.connect(ai[-1])
			await s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))
			if not "Host" in headers:
				await s.write(b"Host: %s\r\n" % host)
			for k in headers:
				await s.write(k)
				await s.write(b": ")
				await s.write(headers[k])
				await s.write(b"\r\n")
			if json is not None:
				assert data is None
				import ujson
				data = ujson.dumps(json)
				await s.write(b"Content-Type: application/json\r\n")
			if data:
				await s.write(b"Content-Length: %d\r\n" % len(data))
			await s.write(b"\r\n")
			if data:
				await s.write(data)

			l = await  s.readline()
			#print(l)
			l = l.split(None, 2)
			status = int(l[1])
			reason = ""
			if len(l) > 2:
				reason = l[2].rstrip()
			while True:
				l = await s.readline()
				if not l or l == b"\r\n":
					break
				#print(l)
				if l.startswith(b"Transfer-Encoding:"):
					if b"chunked" in l:
						raise ValueError("Unsupported " + l)
				elif l.startswith(b"Location:") and not 200 <= status <= 299:
					raise NotImplementedError("Redirects not yet supported")

		else :
			s.connect(ai[-1])
			if proto == "https:":
				s = ussl.wrap_socket(s, server_hostname=host)
			s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))
			if not "Host" in headers:
				s.write(b"Host: %s\r\n" % host)
			# Iterate over keys to avoid tuple alloc
			for k in headers:
				s.write(k)
				s.write(b": ")
				s.write(headers[k])
				s.write(b"\r\n")
			if json is not None:
				assert data is None
				import ujson
				data = ujson.dumps(json)
				s.write(b"Content-Type: application/json\r\n")
			if data:
				s.write(b"Content-Length: %d\r\n" % len(data))
			s.write(b"\r\n")
			if data:
				s.write(data)

			l = s.readline()
			#print(l)
			l = l.split(None, 2)
			status = int(l[1])
			reason = ""
			if len(l) > 2:
				reason = l[2].rstrip()
			while True:
				l = s.readline()
				if not l or l == b"\r\n":
					break
				#print(l)
				if l.startswith(b"Transfer-Encoding:"):
					if b"chunked" in l:
						raise ValueError("Unsupported " + l)
				elif l.startswith(b"Location:") and not 200 <= status <= 299:
					raise NotImplementedError("Redirects not yet supported")
	except OSError:
		if ext == True :
			await s.close()
		else :
			s.close()
		raise

	resp = Response(s)
	resp.status_code = status
	resp.reason = reason
	return resp


async def head(url, **kw):
	return await request("HEAD", url, **kw)

async def get(url, **kw):
	return await request("GET", url, **kw)

async def post(url, **kw):
	return await request("POST", url, **kw)

async def put(url, **kw):
	return await request("PUT", url, **kw)

async def patch(url, **kw):
	return await request("PATCH", url, **kw)

async def delete(url, **kw):
	return await request("DELETE", url, **kw)
