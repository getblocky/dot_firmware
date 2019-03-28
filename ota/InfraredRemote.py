#version=3.0

import sys
core=sys.modules['Blocky.Core']
from machine import Pin , time_pulse_us , PWM
from time import sleep_us , sleep_ms
import os

class InfraredRemote :
    def __init__(self,port,freq=38000):
        self.p = core.getPort(port)
        self.port = port
        self.recv = Pin(self.p[1],Pin.IN)
        self.pwm = PWM(Pin(self.p[0]),duty=0,freq=freq)

        try :
            os.mkdir('IR')
        except OSError :
            pass
        core.deinit_list.append(self)
    
    def deinit(self):
        self.pwm.deinit()
        Pin(self.p[0],Pin.IN)

    def learn(self,name):
        core._failsafeActive(False)
        led = core.indicator.rgb
        led.fill((7,7,0))
        led.write()

        buffer = []
        while True :
            core.gc.collect()
            while self.recv.value() == 0:
                pass
            while self.recv.value() == 1 :
                pass
            pulse = 0
            state = 0
            while pulse > -1 :
      