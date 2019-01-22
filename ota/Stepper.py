#version=1.0
from Blocky.Timer import *
from Blocky.Pin import getPin 
from machine import Pin
from time import sleep_ms
stepper_sequence = [x for x in range(8)]
stepper_sequence[0] = [0,1,0,0]
stepper_sequence[1] = [0,1,0,1]
stepper_sequence[2] = [0,0,0,1]
stepper_sequence[3] = [1,0,0,1]
stepper_sequence[4] = [1,0,0,0]
stepper_sequence[5] = [1,0,1,0]
stepper_sequence[6] = [0,0,1,0]
stepper_sequence[7] = [0,1,1,0]

class Stepper :
	def __init__ (self , port1 , port2 ):
		self.current = 0
		self.phase = 0
		self.target = 0
		self.p1 = getPin(port1)
		self.p2 = getPin(port2)
		if self.p1 == self.p2 : return
		self.A1 = Pin(self.p1[0],Pin.OUT)
		self.A2 = Pin(self.p2[1],Pin.OUT)
		self.B1 = Pin(self.p1[1],Pin.OUT)
		self.B2 = Pin(self.p2[0],Pin.OUT)
		
	def set(self,phase):
		self.A1.value(stepper_sequence[phase][0])
		self.A2.value(stepper_sequence[phase][1])
		self.B1.value(stepper_sequence[phase][2])
		self.B2.value(stepper_sequence[phase][3])
	def step(self ,direction ='clockwise', st