#version=2.0

# The MIT License (MIT)
# Copyright (c) 2015-2018 Volodymyr Shymanskyy
# Copyright (c) 2015 Daniel Campora

"""
	Add support for external socket hook
		+ SIM800L GPRS Networking
		+ A9G
		+ SIM808
"""

import sys;core=sys.modules['Blocky.Core']
from micropython import const
HDR_LEN = const(5)
HDR_FMT = "!BHH"

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
		self._vr_pins[str(pin)] = write

	async def _handle_hw(self,data):
		print('[Blynk] : Handling data ')
		print('[{}]'.format(len(data)) , data)
		try :
			params = list(map(lambda x:x.decode('ascii'),data.split(b'\0')))
			cmd = params.pop(0)
			if cmd == 'vw' or cmd == 'vr':
				pin = int(params.pop(0))

				# Repr channel
				if pin == 127 :
					core.flag.direct_command = True
					try :
						out = eval(params[0])
						if out != None :
							await self.log('[REPR] {}'.format(repr(out)))
					except:
						try :
							exec(params[0])
						except Exception as err:
							await self.log('[EXCEPTION] {}'.format(repr(err)))

				# OTA Channel
				elif pin == 126 :
					print('[{}] OTA Message Received'.format(core.Timer.runtime()))
					core.gc.collect()
					ota_lock = core.eeprom.get('OTA_LOCK')
					if (ota_lock==True and core.cfn_btn.value()==0)or ota_lock != True :
						if core.ota_file == None:
							core.ota_file = open('temp_code.py','w')
							core.ota_file.write(core.prescript)
						if params[1] == 'OTA':
							await core.asyn.Cancellable.cancel_all()
							await core.cleanup()
							await core.indicator.pulse(color = (0,15,25))
							await self.log('[OTA_READY]')

						elif params[1] == "[OTA_CANCEL]":
							if core.ota_file:
								core.ota_file.flush()
								core.ota_file.close()
						else :
							total_part = int(params[1].split('/')[1])
							curre_part = int(params[1].split('/')[0])
							sha1 = core.binascii.hexlify(core.hashlib.sha1(params[0]).digest()).decode('utf-8')
							print('[PART {}/{} , length = {} , sha1 = {}'.format(curre_part,total_part,len(params[0]),sha1))
							if total_part == curre_part:
								core.ota_file.write(params[0])
								core.ota_file.flush()
								core.ota_file.close()
								core.ota_file = None
								core.os.rename('temp_code.py','user_code.py')
								await self.log('[OTA_ACK]' + str([sha1,params[1]]))
								await self.log('[OTA_DONE]')
								print('user code saved')
								#await core.indicator.pulse(color = (0,50,0))
								for x in range(50):
									core.indicator.rgb.fill((0,x,0));core.indicator.rgb.write()
									await core.wait(1)
								for x in range(50,-1,-1):
									core.indicator.rgb.fill((0,x,0));core.indicator.rgb.write()
									await core.wait(1)
								core.mainthread.call_soon(self.ota())
							if curre_part < total_part:
								progress = int(curre_part)%13
								total = int(total_part)%13
								total = 12 if total_part - curre_part > 12 else total
								for x in range(total):
									core.indicator.rgb[x] = (25,0,0)
								for x in range(progress):
									core.indicator.rgb[x] = (0,25,0)
								core.indicator.rgb.write()
								core.ota_file.write(params[0])
								core.ota_file.flush()
								await self.log('[OTA_ACK]'+str([sha1,params[1]]))

					else :
						await self.log('[DOT_ERROR] OTA_LOCKED')

				# User defined channel
				# Note that "vr" and "vw" is the same
				elif (str(pin) in self._vr_pins):
					self.message = params
					for x in range(len(self.message)):
						try :
							self.message[x] = int(self.message[x])
						except :
							pass
					if len(self.message) == 1:
						self.message = self.message[0]
					print('[BLYNK] V{} {} -> {}'.format(pin,type(self.message),self.message))
					if callable(self._vr_pins[str(pin)]):
						await core.call_once('user_blynk_{}_vw'.format(pin),self._vr_pins[str(pin)])
				else :
					print('unregistered channel {}'.format(pin))
		except Exception as err:
			import sys;sys.print_exception(err)
			pass

	def _new_msg_id(self):
		self._msg_id +=1
		self._msg_id = 1 if self._msg_id > 0xFFFF else self._msg_id
		return self._msg_id

	async def _settimeout(self,timeout):
		if timeout != self._timeout:
			self._timeout = timeout
			if self._ext_socket :
				await self.conn.settimeout(timeout)
			else :
				self.conn.settimeout(timeout)

	async def _recv(self,length,timeout=1000):
		await self._settimeout(timeout)

		if length > len(self._rx_data):
			# request more
			try :
				if self._ext_socket :
					self._rx_data += await self.conn.recv(length)
				else :
					self._rx_data += self.conn.recv(length)
			except OSError :
				return b''

		data = self._rx_data[:length]
		print('[blynk] , receiving ' , data , length , "==" , len(data))
		print(self._rx_data)

		self._rx_data = self._rx_data[length:]
		print(self._rx_data)
		print()
		return data

	async def _send(self,data):
		#print('[Blynk] Sending ' , data)
		print('>>> [_send]\t',data)
		retries = 0
		while retries <= MAX_TX_RETRIES:
			try :
				if self._ext_socket :
					await self.conn.send(data)
				else :
					self.conn.send(data)
				self._tx_count += 1
				break
			except OSError as err:
				if err.args[0] != errno.EAGAIN:
					core.flag.blynk = False
					print('[BLYNK] Problem sending data')
					retries += 1
					await core.wait(200)
				else :
					await core.wait(RE_TX_DELAY)

	async def _close(self,emsg=None):
		if self._ext_socket :
			await self.conn.close()
		else :
			self.conn.close()
		self.state = DISCONNECTED
		await core.wait(RECONNECT_DELAY)
		if emsg:
			print('[BLYNK] Error: {}, connection closed'.format(emsg))

	async def _server_alive(self):
		c_time = core.Timer.runtime()
		if self._m_time != c_time:
			self._m_time = c_time
			self._tx_count = 0
			if self._last_hb_id != 0 and c_time - self._hb_time >= MAX_SOCK_TO:
				return False

			if c_time - self._hb_time >= HB_PERIOD and self.state == AUTHENTICATED:
				self._hb_time = c_time
				self._last_hb_id = self._new_msg_id()
				await self._send(core.struct.pack(HDR_FMT,MSG_PING,self._last_hb_id,0))
		return True

	async def notify(self,msg):
		if self.state == AUTHENTICATED:
			await self._send(self._format_msg(MSG_NOTIFY, msg))

	async def tweet(self, msg):
		if self.state == AUTHENTICATED:
			await self._send(self._format_msg(MSG_TWEET, msg))

	async def email(self, email, subject, content):
		if self.state == AUTHENTICATED:
			await self._send(self._format_msg(MSG_EMAIL, email, subject, content))

	async def virtual_write(self,pin,val,device = None):
		if self.state == AUTHENTICATED:
			if device == None:
				await self._send(self._format_msg(MSG_HW, 'vw', pin, val))
			else :
				await self._send(self._format_msg(MSG_BRIDGE ,124, 'i' , device)) # Set channel V124 of this node to point to that device
				await self._send(self._format_msg(MSG_BRIDGE, 124,'vw',  pin , val))

	async def set_property(self, pin, prop, val):
		if self.state == AUTHENTICATED:
			await self._send(self._format_msg(MSG_PROPERTY, pin, prop, val))

	async def log_event(self, event, descr=None):
		if self.state == AUTHENTICATED:
			if descr==None:
				await self._send(self._format_msg(MSG_EVENT_LOG, event))
			else:
				await self._send(self._format_msg(MSG_EVENT_LOG, event, descr))

	async def log(self,message):
		await self.virtual_write(device = self._token.decode('utf-8') , pin = 127 , val = message )
		#await self.virtual_write( pin = 127 , val = message )

	async def sync_all(self):
		if self.state == AUTHENTICATED:
			await self._send(self._format_msg(MSG_HW_SYNC))

	async def sync_virtual(self, pin):
		if self.state == AUTHENTICATED:
			await self._send(self._format_msg(MSG_HW_SYNC, 'vr', pin))

	async def sending(self,to,data):
		await self._send(self._format_msg(MSG_HW,'vw',pin,val))

	async def run(self):
		self._start_time = core.Timer.runtime()
		self._task_millis = self._start_time
		self._hw_pins = {}
		self._rx_data = b''
		self._msg_id = 1
		self._timeout = None
		self._tx_count = 0
		self._m_time = 0
		self.state = DISCONNECTED

		if not self._ext_socket:
			while not core.wifi.wlan_sta.isconnected():
				self.last_call = core.Timer.runtime()
				await core.wait(500)
		while True :
			self._start_time = core.Timer.runtime()
			self.last_call = core.Timer.runtime()
			# Connecting to Blynk Server
			while self.state != AUTHENTICATED:
				try:
					self.last_call = core.Timer.runtime()
					await core.wait(100)
					core.gc.collect()
					core.indicator.show('blynk-connecting')
					self.state = CONNECTING

					if not self._ext_socket :
						print('TCP: Connting to {} : {}'.format(self._server,self._port))
						self.conn = core.socket.socket()
						self.conn.settimeout(1)
					else :
						while core.ext_socket == None:
							await core.wait(500)
						self.conn = core.ext_socket.socket()
						await self.conn.settimeout(2)
					while True :
						try :
							if not self._ext_socket:
								b = core.socket.getaddrinfo(self._server,self._port)[0][4]
								self.conn.connect(b)
								break
							else :
								await self.conn.connect((self._server,self._port))
								break
						except OSError as err:
							import sys;sys.print_exception(err)
							print('>')
							await core.wait(5000)
							continue
					print('Socket: Connected at {}'.format(core.Timer.runtime()))
				except Exception as err:
					core.sys.print_exception(err)
					await self._close('connection with the Blynk servers failed')
					break

				await core.indicator.show('blynk-authenticating')
				self.state = AUTHENTICATING
				hdr = core.struct.pack(HDR_FMT, MSG_LOGIN, self._new_msg_id(), len(self._token))
				print('Blynk connection successful, authenticating...')
				await self._send(hdr+self._token)
				data = await self._recv(HDR_LEN,timeout = MAX_SOCK_TO)
				if not data :
					await self._close('authentication timed out')
					continue
				msg_type, msg_id, status = core.struct.unpack(HDR_FMT, data)
				if status != STA_SUCCESS or msg_id == 0:
					await self._close('authentication failed')
					continue
				await core.indicator.show('blynk-authenticated')
				self.state = AUTHENTICATED
				await self._send(self._format_msg(MSG_INTERNAL, 'ver', '0.1.3', 'buff-in', 4096, 'h-beat', HB_PERIOD, 'dev', core.sys.platform+'-py'))
				print('[Blynk] Connected ! , Happy Blynking :)')
				await core.indicator.pulse(color = (0,40,0))
				core.flag.blynk = True
				await self.log('[BLYNK] Online at {}'.format(core.Timer.current('clock')))

			if self.state == AUTHENTICATED:
				break
		# connection established , perform polling
		self._hb_time = 0
		self._last_hb_id = 0
		self._tx_count = 0
		core.flag.blynk = True
		while True :
			self.last_call = core.Timer.runtime()
			try :
				data = await self._recv(HDR_LEN,NON_BLK_SOCK)
				print('>>> received something' , data)
			except:
				pass
			if data:
				msg_type,msg_id,msg_len = core.struct.unpack(HDR_FMT,data)
				print('type = {} , id = {} , len = {}'.format(msg_type,msg_id,msg_len))
				if msg_id == 0:
					await self._close('invalid msg id : {}'.format(msg_len))
					break
				if msg_type == MSG_RSP:
					if msg_id == self._last_hb_id:
						self._last_hb_id = 0
				elif msg_type == MSG_PING:
					await self._send(core.struct.pack(HDR_FMT,MSG_RSP,msg_id,STA_SUCCESS))
				elif msg_type == MSG_HW or msg_type == MSG_BRIDGE:
					data = await self._recv(msg_len,MIN_SOCK_TO)
					if data :
						await self._handle_hw(data)
				elif msg_type == MSG_INTERNAL :
					await self._recv(msg_len,MIN_SOCK_TO)
				else :
					await self._close('unknown message type')
			else :
				await core.wait(1)

			if not self._server_alive():
				await self._close('blynk server is offline')
				print('[Blynk] Connecting back to server')
				core.flag.blynk = False
				await core.indicator.show('blynk-authenticating')
				return
			else :
				core.flag.blynk = True
			await core.wait(1)
