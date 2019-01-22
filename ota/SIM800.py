#version=1.0
#hash=1123
import sys;core=sys.modules['Blocky.Core'];from micropython import const;from time import ticks_ms as tm;from time import ticks_diff as td;from time import sleep_ms as ts;from machine import UART;s=core.asyncio.sleep_ms;i=isinstance;p=print
F=False;T=True;N=None
def b (d):
	if i(d,bytearray):
		return bytes(d)
	elif i(d,str):
		return bytes(d,'utf-8')
	elif i(d,bytes) or i(d,int):
		return d
class SIM800:
	def __init__(self,port,setting,gprs=F,debug=F):
		self.port=port;self.p=core.getPort(self.port);self.d=debug;self.s=setting;self.fc=F;self.b=b'';self.fr=F;self.fp=F;self.le={};self.lr=N;self.lc=N;self.a=F;self.ls=[N for _ in range(6)]
		self.AF_INET=2;self.AF_INET6=10;self.IPPROTO_IP=0;self.IPPROTO_TCP=6;self.IPPROTO_UDP=17;self.IP_ADD_MEMBERSHIP=3;self.SOCK_DGRAM=2;self.SOCK_RAW=3;self.SOCK_STREAM=1;self.SOL_SOCKET=4095;self.SO_REUSEADDR=4;self.fc=F
		if core.ext_socket==None  or not core.ext_socket.isconnected():
			ext=core.eeprom.get('EXT_SOCKET')
			if ex