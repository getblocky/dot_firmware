#version=2.1

import sys;core=sys.modules['Blocky.Core']
from machine import PWM , Pin
import math

class Servo:
	"""
	A simple class for controlling hobby servos.

	Args:
		pin (machine.Pin): The pin where servo is connected. Must support PWM.
		freq (int): The frequency of the signal, in hertz.
		min_us (int): The minimum signal length supported by the servo.
		max_us (int): The maximum signal length supported by the servo.
		angle (int): The angle between the minimum and maximum positions.

	"""
	def __init__(self, port, freq=50, min_us=600, max_us=2400, angle=180):
		self.min_us = min_us
		self.max_us = max_us
		self.us = 0
		self.freq = freq
		self.maxAngle = angle
		self.port = port
		self.currentAngle = 0
		self.p = core.getPort(port)
		self.pwm = PWM(Pin(self.p[0]), freq=freq, duty=0)
		core.deinit_list.append(self)

	def write_us(self, us):
		"""Set the signal to be ``us`` microseconds long. Zero disables it."""
		if us == 0:
			self.pwm.duty(0)
			return
		us = min(self.max_u