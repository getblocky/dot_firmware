H"

MAX_MSG_PER_SEC = const(1000)

MSG_RSP = const(0)
MSG_LOGIN = const(2)
MSG_PING  = const(6)
MSG_TWEET = const(12)
MSG_EMAIL = const(13)
MSG_NOTIFY = const(14)
MSG_BRIDGE = const(15)
MSG_HW_SYNC = const(16)
MSG_INTERNAL = const(17)
MSG_PROPERTY = const(19)
MSG_HW = const(20)
MSG_EVENT_LOG = const(64)
MSG_REDIRECT  = const(41)  # TODO: not implemented
MSG_DBG_PRINT  = const(55) # TODO: not implemented
STA_SUCCESS = const(200)
HB_PERIOD = const(10000)
NON_BLK_SOCK = const(0)
MIN_SOCK_TO = const(1) # 1 second
MAX_SOCK_TO = const(5000) # 5 seconds, must be < HB_PERIOD
RECONNECT_DELAY = const(1) # 1 second
TASK_PERIOD_RES = const(50) # 50 ms
IDLE_TIME_MS = const(5) # 5 ms
RE_TX_DELAY = const(2)
MAX_TX_RETRIES = const(3)
MAX_VIRTUAL_PINS = const(125)
DISCONNECTED = const(0)
CONNECTING = const(1)
AUTHENTICATING = const(2)
AUTHENTICATED = const(3)
EAGAIN = const(11)

import struct , os , errno
from neopixel import NeoPixel

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
		self.last_call = ticks_ms()
		self.ota = ota
		self._ext_socket = True if True == True else False
		
	def _format_msg(self, msg_type,*args):
		data = ('\0'.join(map(str,args))).encode('ascii')
		return struct.pack(HDR_FMT,msg_type,self._new_msg_id(),len(data)) + data
	
	async def _handle_hw(self,data):
		print('[Blynk] : Handling data ')
		try :
			params = list(map(lambda x:x.decode('ascii'),data.split(b'\0')))
			cmd = params.pop(0)
			if cmd == 'vw' or cmd == 'vr':
				pin = int(params.pop(0))
				
				# Repr channel
				if pin == 127 :
					direct_command = True
					try :
						out = eval(params[0])
						if out !=