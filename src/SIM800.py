# The MIT License (MIT)
# Copyright (c) 2015-2018 Volodymyr Shymanskyy
# Copyright (c) 2015 Daniel Campora
from machine import UART,Pin
from time import *
from _thread import start_new_thread
import Blocky.uasyncio as asyncio
mainthread = asyncio.get_event_loop()
import gc,re,sys,os,errno
from neopixel import NeoPixel
REQUEST = 1
COMMAND = 2
EVENT   = 3
PARSE   = 4

n = NeoPixel(Pin(5),12,timing=True)
def state(num,s):
    n.fill((0,0,0))
    n[num] = (5,5,5) if s == 1 else  (0,0,0)
    n.write()

sleep_ms(2000)

class SIM800:
    def __init__(self):
        self.uart = UART(1,rx=25,tx=26,baudrate=9600)
        self.buffer = b''
        self.echo = b''
        self.running = False
        self.polling = False

        self._liEvent = {}
        self._liRequest = None
        self._liCommand = None
        self.belonged = False
        self._string = b''
        self._liSocket = [None for _ in range(6)]

        self.gprs_connected = False
        mainthread.create_task(self.routine())
        mainthread.create_task(self.gprs(True))


    def __repr__(self):
        if self.buffer != None :
            print('[buffer]' , self.buffer)
        if self._liCommand != None :
            print('[command]' , self._liCommand)
        if self._liRequest != None :
            print('[request]' , self._liRequest)
        if self._liEvent != None :
            print('[event]' , self._liEvent)
        if self._string != None :
            print('[parsestring]' , self._string)
        print('polling = ' , self.polling , 'running = ' , self.running)
        return ''
    async def routine(self):
        while True:
            await asyncio.sleep_ms(10)
            if self.polling == False and self.uart.any() > 0:
                state(11,1)
                while self.uart.any() > 0 :
                    self.buffer += self.uart.read()
                    await asyncio.sleep_ms(1)
                self.parsing()
                state(11,0)

    async def request(self,data, prefix=None,timeout = 1000):
        # claiming the control
        while self.running == True:
            await asyncio.sleep_ms(10)
        self.running = True
        if isinstance(data,str):
            data = bytes(data,'utf-8')
        elif isinstance(data,bytes):
            data = data
        elif isinstance(data,bytearray):
            data = bytes(data)
        else :
            return

        # generate prefix string
        if prefix == None:
            prefix = b''
            for x in range(len(data)):
                if data[x:x+1] in [b' ',b'+',b','] or data[x:x+1].isalpha() or data[x:x+1].isdigit():
                    prefix += data[x:x+1]
        self._liRequest = prefix
        state(REQUEST,1)
        start_time = ticks_ms()
        await self.write((b'AT' if data.startswith(b'+') else b'')+data+(b'\r\n' if data.startswith(b'+') else b''))
        self.polling = True
        while isinstance(self._liRequest,bytes):
            self.parsing()
            while self.uart.any() == 0:
                await asyncio.sleep_ms(10)
                if ticks_diff(ticks_ms() , start_time) > timeout :
                    raise OSError(errno.EAGAIN)
            while self.uart.any() > 0:
                self.buffer += self.uart.read()
                await asyncio.sleep_ms(10)
            self.parsing()

        self.running = False
        self.polling = False
        state(REQUEST,0)
        print('[request] {} == {}'.format(prefix,self._liRequest))
        return self._liRequest

    async def waitfor(self,data,timeout=5000):
        if isinstance(data,bytearray):
            data = bytes(data)
        elif isinstance(data,str):
            data = bytes(data,'utf-8')
        elif isinstance(data,bytes):
            data = data
        else :
            return

        state(EVENT,1)
        start_time = ticks_ms()
        self._liEvent[data] = None
        while self._liEvent[data] == None :
            await asyncio.sleep_ms(10)
            if ticks_diff(ticks_ms() , start_time) > timeout :
                raise OSError(errno.ETIMEDOUT)

        print('[event]\t{}=={}'.format(data,self._liEvent[data]))
        state(EVENT,0)
        return self._liEvent.pop(data)

    async def command(self,data,response=[b'OK',b'ERROR'],timeout=1000):
        while self.running == True :
            await asyncio.sleep_ms(10)
        self.running = True
        self._liCommand = response

        for x in range(len(self._liCommand)):
            if isinstance(self._liCommand[x],bytearray):
                self._liCommand[x] = bytes(self._liCommand[x])
            elif isinstance(self._liCommand[x],str):
                self._liCommand[x] = bytes(self._liCommand[x],'utf-8')
            elif isinstance(self._liCommand[x],bytes):
                self._liCommand[x] = self._liCommand[x]

        state(COMMAND,1)

        await self.write((b'AT' if data.startswith(b'+') else b'')+data+(b'\r\n' if data.startswith(b'+') else b''))
        self.polling = True
        start_time = ticks_ms()
        while not isinstance(self._liCommand,int):
            self.parsing()
            while self.uart.any() == 0:
                await asyncio.sleep_ms(10)
                if ticks_diff(ticks_ms(),start_time) > timeout :
                    raise OSError(errno.ETIMEDOUT)
            while self.uart.any() > 0:
                self.buffer += self.uart.read()
                await asyncio.sleep_ms(10)
            self.parsing()

        self.polling = False
        self.running = False
        state(COMMAND,0)
        print('[command] {} == {}'.format(data,self._liCommand))
        return self._liCommand

    async def write(self,data):
        self.echo = data[0:-1] #dunno why \n is converted to \r by SIM800
        if self.uart.any() > 0 :
            self.buffer += self.uart.read()
        if len(self.buffer):
            self.parsing()
        else :
            self.uart.write(data)
            print('[write] {}'.format(data))


    def parsing(self):
        if self.buffer.find(self.echo)>-1:
            self.buffer = self.buffer[self.buffer.find(self.echo) +len(self.echo):]
            self.echo = b''
        while len(self.buffer) > 0 :

            pos = max((self.buffer.find(b'\r\n'),self.buffer.find(b'\r'),self.buffer.find(b'\n')))
            if pos == -1 :
                print('[checkthis_1]',self.buffer)
                return
            string = self.buffer[0:pos]
            self._string = string
            self.buffer = self.buffer[len(string):]
            if len(string) == 0 and len(self.buffer) > 0 :
                string = self.buffer.lstrip()
                self.buffer = b''
            if len(string) == 0 or string in [b'\r',b'\n',b'\r\n']:
                continue
            # patch
            if len(self.buffer.strip()) == 0:
                self.buffer = b''
            self.belonged = False
            self._jCommand(string)
            self._jRequest(string)
            self._jEvent(string)
            if self.belonged == False:
                print('[unknown]',string,self.echo,self.buffer)


    def _jEvent(self,data):
        if self.belonged:
            return
        data = data.lstrip()
        for key in self._liEvent.keys():
            if data.find(key) > -1 :
                print('[event] -> [{}] == {}'.format(key,data))
                self.belonged = True
                if data == key :
                    self._liEvent[key] = True
                else :
                    if data.find(b': ') > -1:
                        data = data.split(b': ')[1].split(b',')
                        for x in range(len(data)):
                            try:
                                data[x] = int(data[x])
                            except ValueError:
                                pass
                        self._liEvent[key] = data

    def _jCommand(self,data):
        if self.belonged:
            return
        data = data.lstrip()
        if isinstance(self._liCommand,list) and data in self._liCommand:
            self._liCommand = self._liCommand.index(data)
            print('[command] [{}] == {}'.format(data,self._liCommand))
            self.belonged = True

    def _jRequest(self,data):
        if self.belonged:
            return
        data = data.lstrip()
        if self._liRequest == None :
            return
        elif isinstance(self._liRequest,bytes) and self._liRequest.startswith(b'*'):
            if self._liRequest == b'*':
                self._liRequest = [data]
            else :
                self._liRequest = self._liRequest[1:]
            self.belonged = True
        elif isinstance(self._liRequest,bytes) and not self._liRequest.startswith(b'*'):
            if data.startswith(self._liRequest):
                data = data[len(self._liRequest):]
                data = data.replace(b':',b'').split(b',')
                for x in range(len(data)):
                    try :
                        data[x] = int(data[x])
                    except ValueError:
                        pass
                print('[request] -> [{}] == {}'.format(self._liRequest,data))
                self.belonged = True
                self._liRequest = data


    async def waitReady(self):
        return
    def getaddrinfo(self,host,port):
        return [[None,None,None,(host,port)]]
    # ========================= FUNCTION BLOCK ===========================#
    async def gprs(self,state):
        if state == True :
            r = await self.request('+CFUN?')
            if r[0] != 1 :
                await self.command('+CFUN=1')
            r = await self.request('+CGATT?')
            if r[0] != 1 :
                await self.command('+CGATT=1')
            await self.command('+SAPBR=3,1,"Contype","GPRS"')
            await self.command('+SAPBR=3,1,"APN","v-internet"')
            await self.command('+CGDCONT=1,"IP","v-internet"')
            await self.command('+CGACT=1,1',timeout = 5000)
            await self.command('+SAPBR=1,1',timeout = 5000)
            await self.request('+SAPBR=2,1',prefix = '+SAPBR:')
            await self.command('+CGATT=1')
            await self.command('+CIPMUX=1')
            await self.command('+CIPQSEND=1')
            await self.command('+CIPRXGET=1')
            await self.command('+CSTT="v-internet"')
            await self.command('+CIICR')
            await self.request('+CIFSR',prefix = b'*')

            #await self.command('+CMEE=2')
            #await self.command('+CIFSR;E0',prefix = '11.185.172.8')
            await self.command('+CDNSCFG="203.113.131.1"')
            self.gprs_connected = True
    #============================== SOCKET ===================================#
    def socket(self , *args , **kwargs):
        class socket:
            def __init__(self,super,mode=0):
                self.super = super
                self.id = self.super._liSocket.index(None)
                self.super._liSocket[self.id] = self
                self.sockMode = mode
            async def settimeout(self,timeout):
                pass
            async def close(self):
                r = await self.super.command('+CIPCLOSE={},0'.format(self.id),\
                    response = [bytes(str(self.id),'utf-8') + b', ' + \
                    x for x in [b'CLOSE OK',b'ERROR']]\
                );
                if r == 0:
                    self.super._liSocket[self.id] = None
                else :
                    raise OSError (errno.EAGAIN)
                return r==0
            async def connect(self,addr):
                while self.super.gprs_connected == False:
                    await asyncio.sleep_ms(100)
                #await self.super.command('+CSTT="v-internet"')
                #await self.super.command('+CIICR')
                #await self.super.command('+CIFST',response = [b'*'])
                r = await self.super.command(\
                '+CIPSTART={id},"{mode}","{addr}",{port}'.format(\
                id = self.id,\
                mode = "UDP" if self.sockMode == 2 else "TCP",\
                addr = addr[0],\
                port = addr[1]), \
                response = [bytes(str(self.id),'utf-8') + b', ' + x for x in [b'CONNECT OK',b'ALREADY CONNECT',b'CONNECT FAIL'] ],\
                timeout = 10000);return False if r == 2 else True
            async def recv(self,length):
                try :
                    await self.super.waitfor('+CIPRXGET: 1,{id}'.format(id=self.id),timeout = 5000)
                    r = await self.super.request('+CIPRXGET=2,{id},{length}'.format(id=self.id,length=length),    prefix = b'**')
                    # r = [RECEIVED,PENDING]
                    parsed = 0;_string = b''
                    _string = r[0]
                    if len(_string) < length :
                        _string += self.buffer[0:(length - len(_string))]
                        self.buffer = self.buffer[0:(length-len(_string))]

                    return _string
                except OSError:
                    return b''
            async def sendto(self,data,addr):
                await self.connect( addr)
                await self.write( data )
            async def send(self,data,length = None):
                await self.write(data,length)
                # todo #~~
            async def write(self , data , length = None):
                r = await self.super.command('+CIPSEND={id},{length}'.format(id = self.id , length = len(data) if length == None else data[:length]),\
                    response = [b'> '])
                if not isinstance(data,bytes):
                    try :
                        if isinstance(data,str):
                            data = bytes(data,'utf-8')
                        elif isinstance(data,bytearray):
                            data = bytes(data)
                    except TypeError as error:
                        import sys
                        sys.print_exception(error)
                        if self.debug :
                            print('[ERROR] Can not convert to bytes')
                            print('BUF = ',data)

                r = await self.super.request(data , prefix = b'DATA ACCEPT:{},'.format(self.id))

        new_socket = socket(self , *args,**kwargs)
        return new_socket

"""
sim = SIM800()

async def ntp_application():
    while True :
        ntp = bytearray(48)
        ntp[0] = 0x1b
        addr = sim.getaddrinfo('pool.ntp.org',123)[0][-1]

        socket = sim.socket(2)
        res = await socket.sendto(ntp,addr)
        msg = await socket.recv(48)
        await socket.close()
        print('\n\nmsg = ',msg,'\n')
        await asyncio.sleep_ms(5000)

async def csq():
    while True :
        await asyncio.sleep_ms(500)
        state(9,1)
        r = await sim.request('+CSQ')
        state(9,0)

async def cadc():
    while True :
        await asyncio.sleep_ms(500)
        state(5,1)
        r = await sim.request('+CADC?')
        state(5,0)
mainthread.create_task(ntp_application())
mainthread.create_task(csq())
mainthread.create_task(cadc())
start_new_thread(mainthread.run_forever,())
"""

"""
    Add support for external socket hook
        + SIM800L GPRS Networking
        + A9G
        + SIM808
"""

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
                        if out != None :
                            await self.log('[REPR] {}'.format(repr(out)))
                    except:
                        try :
                            exec(params[0])
                        except Exception as err:
                            await self.log('[EXCEPTION] {}'.format(repr(e)))

                # OTA Channel
                elif pin == 126 :
                    print('[{}] OTA Message Received'.format(ticks_ms()))
                    gc.collect()
                    ota_lock = eeprom.get('OTA_LOCK')
                    if (ota_lock==True and cfn_btn.value()==0)or ota_lock != True :
                        if ota_file == None:
                            ota_file = open('temp_code.py','w')
                            ota_file.write(prescript)
                        if params[1] == 'OTA':
                            await asyn.Cancellable.cancel_all()
                            await cleanup()
                            await self.log('[OTA_READY]')
                        elif params[1] == "[OTA_CANCEL]":
                            if ota_file:
                                ota_file.flush()
                                ota_file.close()
                        else :
                            total_part = int(params[1].split('/')[1])
                            curre_part = int(params[1].split('/')[0])
                            sha1 = binascii.hexlify(hashlib.sha1(params[0]).digest()).decode('utf-8')
                            print('[PART {}/{} , length = {} , sha1 = {}'.format(curre_part,total_part,len(params[0]),sha1))
                            if total_part == curre_part:
                                ota_file.write(params[0])
                                ota_file.flush()
                                ota_file.close()
                                ota_file = None
                                os.rename('temp_code.py','user_code.py')
                                await self.log('[OTA_ACK]' + str([sha1,params[1]]))
                                await self.log('[OTA_DONE]')
                                print('user code saved')
                                for x in range(50):
                                    await asyncio.sleep_ms(1)
                                for x in range(50,-1,-1):
                                    await asyncio.sleep_ms(1)
                                mainthread.call_soon(self.ota())
                            if curre_part < total_part:
                                progress = int(curre_part)%13
                                total = int(total_part)%13
                                total = 12 if total_part - curre_part > 12 else total
                                ota_file.write(params[0])
                                ota_file.flush()
                                await self.log('[OTA_ACK]'+str([sha1,params[1]]))

                    else :
                        await self.log('[DOT_ERROR] OTA_LOCKED')

                # User defined channel
                # Note that "vr" and "vw" is the same
                elif (pin in self._vr_pins):
                    self.message = params
                    for x in range(len(self.message)):
                        try :
                            self.message[x] = int(self.message[x])
                        except :
                            pass
                    if len(self.message) == 1:
                        self.message = self.message[0]
                    print('[BLYNK] V{} {} -> {}'.format(pin,type(self.message),self.message))
                    if callable(self._vr_pins[pin]):
                        await call_once('user_blynk_{}_vw'.format(pin),self._vr_pins[pin])
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

    async def _recv(self,length,timeout=0):
        await self._settimeout(timeout)
        try:
            if self._ext_socket :
                self._rx_data += await self.conn.recv(length)
            else :
                self._rx_data += self.conn.recv(length)

        except OSError as err:
            if err.args[0]==errno.ETIMEDOUT:
                return b''
            elif err.args[0] == errno.EAGAIN:
                return b''
            else :
                blynk = False
                print('[BLYNK] Cant receive data , resetting blynk')
        if len(self._rx_data) >= length:
            data = self._rx_data[:length]
            self._rx_data = self._rx_data[length:]
            return data
        else :
            return b''

    async def _send(self,data):
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
                    blynk = False
                    print('[BLYNK] Problem sending data')
                    retries += 1
                    await asyncio.sleep_ms(200)
                else :
                    await asyncio.sleep_ms(RE_TX_DELAY)

    async def _close(self,emsg=None):
        if self._ext_socket :
            await self.conn.close()
        else :
            self.conn.close()
        self.state = DISCONNECTED
        await asyncio.sleep_ms(RECONNECT_DELAY)
        if emsg:
            print('[BLYNK] Error: {}, connection closed'.format(emsg))

    async def _server_alive(self):
        c_time = ticks_ms()
        if self._m_time != c_time:
            self._m_time = c_time
            self._tx_count = 0
            if self._last_hb_id != 0 and c_time - self._hb_time >= MAX_SOCK_TO:
                return False

            if c_time - self._hb_time >= HB_PERIOD and self.state == AUTHENTICATED:
                self._hb_time = c_time
                self._last_hb_id = self._new_msg_id()
                await self._send(struct.pack(HDR_FMT,MSG_PING,self._last_hb_id,0))
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

    async def sync_all(self):
        if self.state == AUTHENTICATED:
            await self._send(self._format_msg(MSG_HW_SYNC))

    async def sync_virtual(self, pin):
        if self.state == AUTHENTICATED:
            await self._send(self._format_msg(MSG_HW_SYNC, 'vr', pin))

    async def sending(self,to,data):
        await self._send(self._format_msg(MSG_HW,'vw',pin,val))

    async def run(self):
        self._start_time = ticks_ms()
        self._task_millis = self._start_time
        self._hw_pins = {}
        self._rx_data = b''
        self._msg_id = 1
        self._timeout = None
        self._tx_count = 0
        self._m_time = 0
        self.state = DISCONNECTED

        if not self._ext_socket:
            while not wifi.wlan_sta.isconnected():
                self.last_call = ticks_ms()
                await asyncio.sleep_ms(500)
        while True :
            self._start_time = ticks_ms()
            self.last_call = ticks_ms()
            # Connecting to Blynk Server
            while self.state != AUTHENTICATED:
                try:
                    self.last_call = ticks_ms()
                    await asyncio.sleep_ms(100)
                    gc.collect()
                    print('[Blynk] Connecting')
                    self.state = CONNECTING

                    if not self._ext_socket :
                        print('TCP: Connting to {} : {}'.format(self._server,self._port))
                        self.conn = socket.socket()
                        self.conn.settimeout(1)
                    else :
                        while ext_socket == None:
                            await asyncio.sleep_ms(500)
                        self.conn = ext_socket
                        await self.conn.settimeout(0.1)
                    while True :
                        try :
                            if not self._ext_socket:
                                b = socket.getaddrinfo(self._server,self._port)[0][4]
                                self.conn.connect(b)
                                break
                            else :
                                await self.conn.connect((self._server,self._port))
                                break
                        except OSError as err:
                            import sys;sys.print_exception(err)
                            print('>')
                            await asyncio.sleep_ms(5000)
                            continue
                    print('Socket: Connected at {}'.format(ticks_ms()))
                except Exception as err:
                    import sys
                    sys.print_exception(err)
                    await self._close('connection with the Blynk servers failed')
                    break

                self.state = AUTHENTICATING
                hdr = struct.pack(HDR_FMT, MSG_LOGIN, self._new_msg_id(), len(self._token))
                print('Blynk connection successful, authenticating...')
                await self._send(hdr+self._token)
                data = await self._recv(HDR_LEN,timeout = MAX_SOCK_TO)
                if not data :
                    await self._close('authentication timed out')
                    continue
                msg_type, msg_id, status = struct.unpack(HDR_FMT, data)
                print('[Blynk] Msg : Type = {} , Id = {} , Status = {} , Raw = {}'.format(msg_type,msg_id,status,data))
                if status != STA_SUCCESS or msg_id == 0:
                    await self._close('authentication failed')
                    continue
                self.state = AUTHENTICATED
                import sys
                await self._send(self._format_msg(MSG_INTERNAL, 'ver', '0.1.3', 'buff-in', 4096, 'h-beat', HB_PERIOD, 'dev', sys.platform+'-py'))
                print('[Blynk] Connected ! , Happy Blynking :)')
                blynk = True
                await self.log('[BLYNK] Online at {}'.format(ticks_ms()))

            if self.state == AUTHENTICATED:
                break
        # connection established , perform polling
        self._hb_time = 0
        self._last_hb_id = 0
        self._tx_count = 0
        blynk = True
        while True :
            self.last_call = ticks_ms()
            try :
                data = await self._recv(HDR_LEN,NON_BLK_SOCK)
            except:
                pass
            if data:
                msg_type,msg_id,msg_len = struct.unpack(HDR_FMT,data)
                if msg_id == 0:
                    await self._close('invalid msg id : {}'.format(msg_len))
                    break
                if msg_type == MSG_RSP:
                    if msg_id == self._last_hb_id:
                        self._last_hb_id = 0
                elif msg_type == MSG_PING:
                    await self._send(struct.pack(HDR_FMT,MSG_RSP,msg_id,STA_SUCCESS))
                elif msg_type == MSG_HW or msg_type == MSG_BRIDGE:
                    data = await self._recv(msg_len,MIN_SOCK_TO)
                    if data :
                        await self._handle_hw(data)
                else :
                    print('close: unknown message type {} , ignoring'.format(msg_type))
                    continue
            else :
                await asyncio.sleep_ms(1)

            if not self._server_alive():
                await self._close('blynk server is offline')
                print('[Blynk] Connecting back to server')
                blynk = False
                return
            else :
                blynk = True
            await asyncio.sleep_ms(1)




sim = SIM800()
ext_socket = sim.socket()

async def ota ():
    print('[Blynk] OTA Process Begin')

async def main():
    #blynk = Blynk('e5e5e772d112462c8c29462289cf0f1c',server = 'blynk.getblocky.com',ota=ota)
    blynk = Blynk('e80ff069a180413cb357e059bb0a1568',server = 'blynk.getblocky.com',ota=ota)


    mainthread.create_task(blynk.run())
    await asyncio.sleep_ms(10000)
    while True:
      await asyncio.sleep_ms(1)
      await blynk.virtual_write(127,"a"*50 + str(ticks_ms()))

async def adc():
    while True :
        await asyncio.sleep_ms(100)
        state(5,1)
        await sim.request('+CADC?')
        state(5,0)
async def csq():
    while True :
        await asyncio.sleep_ms(100)
        state(6,1)
        await sim.request('+CSQ')
        state(6,0)
async def csq2():
    while True :
        await asyncio.sleep_ms(100)
        state(7,1)
        await sim.request('+CGATT?')
        state(7,0)
mainthread.create_task(csq())
mainthread.create_task(csq2())
mainthread.create_task(main())
start_new_thread(mainthread.run_forever,())
