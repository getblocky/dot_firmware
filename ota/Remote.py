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
				x |=