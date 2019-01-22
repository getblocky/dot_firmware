#version=1.0
#from blocky_utility import get_free_UART TODO
import machine , time
def getPort(a):
	return 25 , 26 , None 
class Music :
	def __init__ ( self , port ):
		self.port = port
		self.p = getPort(port)
		if (self.p[0]==None or self.p[1] == None):
			return
		self.bus = None
	
	def sendStack(self , cmd , param1 , param2):
		# plug and play
		self.bus = machine.UART(1 , 9600)
		self.bus.init(baudrate = 9600 , bits = 8 , parity = None , stop = 1 , rx = self.p[0] , tx = self.p[1] )
		# empty the buffer
		while self.bus.any():
			self.bus.read()
			
		buff = bytearray([0x7E, 0xFF, 0x06, cmd,0x00, param1, param2, 0xEF])
		#if self.bus.write(buff) == len(buff):
		#	self.bus.deinit()
		self.bus.write(buff) 
		nowTime = time.ticks_ms()
		print('SEND : ',end='')
		for x in buff:
			print(hex(x),end = '\t')
		print()
		
		# no ack 

	def _readRegister(self,cmd,param=None):
		# plug and play
		self.bus = machine.UART(1 , 9600)
		self.bus.init(baudrate = 9600 , bits = 8 , parity = None , s