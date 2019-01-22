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
		proto, dummy, host, path = url.split(