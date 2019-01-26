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
			bit_prev = self._decode()
			bit_curr = 0
			self._clear()
			last_attempt = 0
			while True:
				h(None)

				if (self.length and self.prev_irq and d(u() , self.prev_irq) > 500000):

					print('__')
					last_attempt = u()
					self._correct()
					if self.length//2 != bit_length :
						core.indicator.rgb.fill((10,0,0));core.indicator.rgb.write()
						sleep_ms(10)
						core.indicator.rgb.fill((0,0,0));core.indicator.rgb.write()
						print('differet length' , self.length//2 , bit_length)
						self._debug()
						self._clear()
						continue
					bit_curr = self._decode()
					if bit_curr == bit_prev :
						core.indicator.rgb.fill((0,10,0));core.indicator.rgb.write()
						sleep_ms(10)
						core.indicator.rgb.fill((0,0,0));core.indicator.rgb.write()
						print('same' , bit_curr)
						self._clear()
						continue

					print('RECV {}'.format(self.length))
					print('Current bit mask = ' , bin(bit_mask))
					for x in range(bit_length):
						print('[C] {}      {} == {}'.format(x , self._bit(bit_curr,x),self._bit(bit_prev,x)),end='')
						if self._bit(bit_curr,x) != self._bit(bit_prev,x):
							bit_mask = self._bit(bit_mask,x,0)
							print('###')
						else :
							print()
					print('BIT_MASK ' , bin(bit_mask))

					bit_prev = bit_curr
					self._clear()

				if (last_attempt and d(u() , last_attempt) > 3000000):
					break
			print('final bit mask = {}'.format(bin(bit_mask)))

			core._failsafeActive(True)
			self._recvActive(True)

			return
			if isinstance(name , str):
				self.learning = name
				print("[remote] Learning signal .. {} .. ".format(name))
		except Exception as err:
			import sys
			sys.print_exception(err)
	def _handler (self , source):
		if self.recv.value()!= self.last_state:
			self.last_state = not self.last_state
			self.time = ticks_us()
			if self.prev_irq == 0 :
				self.prev_irq = self.time
				return
			self.buffer[self.length] = min(255,ticks_diff(self.time,self.prev_irq)//50)
			self.length += 1
			self.prev_irq = self.time


	def _correct(self):
		pos = 0
		length = self.length
		while True :
			if (self.buffer[0] < self.buffer[1] and self.buffer[0] *2 < self.buffer[1]) or self.buffer[0] > 20000:
				print('correct')
				length -= 1
				for x in range(0 , length):
					self.buffer[x] = self.buffer[x+1]
			else :
				break



	@core.asyn.cancellable
	async def _routine (self):
		while True :
			await core.wait(1000)
			if self.length > 0 and core.time.ticks_diff(core.time.ticks_us() , self.prev_irq) > 1000000:
				self._recvActive(False)
				self._correct()
				self.bin = self._decode(self.buffer , self.length)
				if self.learning :
					self._store (self.learning , self.buffer , self.bin , self.length)
					print("[remote] Signal ..{}.. is learnt".format(self.learning))
					self.learning = None
				else :
					name = self._recognise(self.bin)
					if name :
						core.mainthread.call_soon(core.call_once("user_remote_{}_{}".format(self.port, name),self.event_list[name][1]))

				self._debug()
				sleep_ms(1000)
				self.send(self.buffer , self.length)
				self.length = 0
				self.prev_irq = 0
				for x in range(len(self.buffer)):
					self.buffer[x] = 0
				self._recvActive(True)


	def _debug(self):
		print("__________________RECV	{}	______ {} _______".format(self.length , self.bin))
		for x in range(self.length//8) :
			for i in range(8):
				print(self.buffer[x*8+i]*50 , end = "\t" if	self.buffer[x*8+i]*50 > 300 else "#\t")
			print()
		for x in range(self.length%8):
			print( self.buffer[self.length//8 + x]*50 , end = "\t" if	self.buffer[self.length//8 + x]*50 > 300 else "#\t")

		print("------------------------------------------")



	def _recvActive(self , state):
		if state == True :
			self.recv = core.machine.Pin(self.p[1] , core.machine.Pin.IN , core.machine.Pin.PULL_UP)
			self.recv.irq(trigger = core.machine.Pin.IRQ_RISING|core.machine.Pin.IRQ_FALLING , handler = self._handler)
		elif state == False :
			self.recv.irq(trigger = 0 , handler = None)
			self.recv = core.machine.Pin(self.p[1] , core.machine.Pin.IN)
		core.time.sleep_ms(5)

	def _store(self , name , packet , bin , length = None):
		meta_data = {"bin":bin , "length": length or len(packet) , "protocol" : "RAW"}
		with open("IR/{}.txt".format(name),"w") as fp :
			fp.write(core.json.dumps(meta_data))
			fp.write("\n")
			for x in range(length or len(packet)):
				fp.write(str(packet[x]))
				fp.write("," if x%2==0 else "\n")

	def _load(self , name , include_raw = False):
		meta_data = {}
		data = bytearray(1000)
		with open("IR/{}.txt".format(name)) as fp:
			line = fp.readline()
			meta_data = core.json.loads(line)

			if not include_raw :
				return meta_data["length"] , meta_data["bin"] , None
			pos = 0
			while line:
				line = fp.readline()
				try :
					data[pos] = (int(line.split(",")[0]))
					pos += 1
				except :
					pass
				try :
					data[pos] =	(int(line.split(",")[1]))
					pos += 1
				except :
					pass

			return meta_data["length"] , meta_data["bin"] , data

	def _learned(self , name):
		if "{}.txt".format(name) in core.os.listdir("IR"):
			return True
		return False

	def _recognise(self , bin):
		for x in self.event_list :
			if self.event_list[x]["bin"] == bin :
				return x
		return None

	def _decode(self , packet = None, length = None):
		binary = 0
		m = 500000
		if length == None and packet == None :
			length = self.length
			packet = self.buffer
		else :
			length = length or len(packet)
		for x in range(length):
			m = min(packet[x] , m)
		for x in range(0 , length , 2):
			if packet[x+1] > packet[x]*2 :
				binary += 2**(x//2)
		return binary


	# User exposed function


	def event (self , name , function):
		if self._learned(name):
			self.event_list[name] = [self._load(name)]

	def send ( self , name , length = None):
		self._recvActive(False)
		packet = []
		length = 0

		if isinstance(name , str):
			length , _ ,	packet = self._load(name,True)
		if isinstance(name , bytearray):
			length = length or len(name)
			packet = name
		duty = self.pwm.duty
		sleep = core.time.sleep_us
		self.recv.irq(trigger = 0,handler = None)
		sleep(1000)
		for x in range(length):
			duty(512 if x%2==0 else 0)
			sleep(packet[x]*50)
		duty(0)
		sleep(3000)
		self._recvActive(True)

	async def get_learned(self):
		print('[REMOTE_LEARNED] {}'.format([x.split('.')[0] for x in core.os.listdir('IR')]))
		while core.flag.blynk == False :
			await core.wait(200
		await core.blynk.log(
