#version=2.0

import sys;core = sys.modules["Blocky.Core"]
from time import *
class Remote:
	def __init__(self,port):
		self.p	= core.getPort(port)
		self.port = port
		self.recv = core.machine.Pin(self.p[1] , core.machine.Pin.IN , core.machine.Pin.PULL_UP)
		self.pwm = core.machine.PWM(core.machine.Pin(self.p[0]) , duty = 0 , freq = 38000)
		self._recvActive(True)
		# Initialize Buffer , see ISR note !
		self.buffer = bytearray(1000)
		self.bin = 0
		self.length = 0
		
		# Initialize Timing Property
		self.prev_irq = 0
		self.time = 0
		
		# Initialize User Interface
		self.learning = None 
		self.event_list = {}
		
		self.last_state = 1
		core.mainthread.create_task(core.asyn.Cancellable(self._routine)())
		
		try :
			core.os.mkdir("IR")
		except OSError:
			pass
			
	def _bit(self , x , n , value = None):
		if value != None:
			mask = 1 << n   # Compute mask, an integer with just bit 'index' set.
			x &= ~mask          # Clear the bit indicated by the mask (if x is False)
			if value:
				x |= mask         # If x was True, set the bit indicated by the mask.
			return x
		else:
			return 1 if x & 2 ** n != 0  else 0
	
	
	def _clear(self):
		# clear
		self.length = 0
		for x in range(len(self.buffer)):
			self.buffer[x] = 0
		self.prev_irq = 0
	
	def learn(self , name):
		try :
			self.last_state = self.recv.value()
			print("LEARNING")
			self._recvActive(False)
			core._failsafeActive(False)
			# learning the raw code , this is used for sending
			self._clear()
			h = self._handler
			d = ticks_diff
			u = ticks_us
			while not (d(u() , self.prev_irq) > 500000 and self.length) :
				h(None)
			self._correct()
			with open('IR/{}.txt'.format(name), 'w') as fp:
				for x in range(self.length):
					fp.write(str(self.buffer[x]))
					fp.write('\n')
			print('Raw data written = {}'.format(self.length))
			self._debug()
			# perform bit mask operation
			bit_length = self.length //2
			bit_mask = 0
			for x in range(bit_length):
				bit_mask += 2**x
			bit_prev = sel