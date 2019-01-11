from machine import UART,Pin
from time import *
from _thread import start_new_thread
import Blocky.uasyncio as asyncio
mainthread = asyncio.get_event_loop()
import gc,re,sys,os
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
                while self.uart.read() > 0 :
                    self.buffer += self.uart.read()
                    await asyncio.sleep_ms(1)
                self.parsing()

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
                    raise OSError
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
                raise OSError

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
                    raise OSError
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
        self.echo = data[0:-1]
        if self.uart.any() > 0 :
            self.buffer += self.uart.read()
        if len(self.buffer):
            self.parsing()
        else :
            self.uart.write(data)
            print('[write] {}'.format(data))


    def parsing(self):
        if self.buffer.startswith(self.echo):
            self.buffer = self.buffer[len(self.echo):]
            self.echo = b''
        while len(self.buffer) > 0 :

            pos = max((self.buffer.find(b'\r\n'),self.buffer.find(b'\r'),self.buffer.find(b'\n')))
            if pos == -1 :
                print('[checkthis_1]',self.buffer)
                return
            string = self.buffer[0:pos]
            self._string = string
            self.buffer = self.buffer[len(string):]
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
                print('[unknown]',string)


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
            await self.command('+CGACT=1,1')
            await self.command('+SAPBR=1,1')
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

            async def close(self):
                r = await self.super.command('+CIPCLOSE={},0'.format(self.id),\
                    response = [bytes(str(self.id),'utf-8') + b', ' + \
                    x for x in [b'CLOSE OK',b'ERROR']]\
                );return r==0
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
                await self.super.waitfor('+CIPRXGET: 1,{id}'.format(id=self.id))
                r = await self.super.request('+CIPRXGET=2,{id},{length}'.format(id=self.id,length=length),    prefix = b'**')
                # r = [RECEIVED,PENDING]
                if r[0] == length:
                    return #TODO ERROR HERE
                return r
            async def sendto(self,data,addr):
                await self.connect( addr)
                await self.write( data )

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

                r = await self.super.request(data , prefix = b'DATA ACCEPT:{},'.format(self.id),iscmd=True)

        new_socket = socket(self , *args,**kwargs)
        return new_socket


sim = SIM800()

async def ntp_application():
    while True :
        ntp = bytearray(48)
        ntp[0] = 0x1b
        addr = sim.getaddrinfo('pool.ntp.org',123)[0][-1]

        socket = sim.socket(2)
        res = await socket.sendto(ntp,addr)
        msg = await socket.recv(48)
        socket.close()
        print('\n\nmsg = ',msg,'\n')
        await asyncio.sleep_ms(5000)

mainthread.create_task(ntp_application())
start_new_thread(mainthread.run_forever,())
