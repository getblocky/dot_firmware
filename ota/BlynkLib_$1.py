
RE_TX_DELAY = const(2)
MAX_TX_RETRIES = const(3)
MAX_VIRTUAL_PINS = const(125)
DISCONNECTED = const(0)
CONNECTING = const(1)
AUTHENTICATING = const(2)
AUTHENTICATED = const(3)
EAGAIN = const(11)



class Blynk:
	def __init__(self, token, server='blynk.getblocky.com', port=None, connect=True, ssl=False,ota=None):
		self._vr_pins = {}
		self._token = token.encode('ascii') if isinstance(token,str) else token
		self.message = None
		self._server = server
		if port is None :
			if ssl :
				port = 8441
			else :
				port = 80
		self._port = port
		self._ssl = ssl
		self.state = DISCONNECTED
		self.conn = None
		self._timeout = None
		self.last_call = core.Timer.runtime()
		self.ota = ota
		self._ext_socket = True if core.eeprom.get('EXT_SOCKET') == True else False

	def _format_msg(self, msg_type,*args):
		data = ('\0'.join(map(str,args))).encode('ascii')
		return core.struct.pack(HDR_FMT,msg_type,self._new_msg_id(),len(data)) + data

	def add_virtual_pin(self, pin , write):
		self._vr_pin