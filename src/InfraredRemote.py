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
                pulse = time_pulse_us(self.recv,state,100000)
                buffer.append(pulse)
                state = not state
            buffer.pop() 

            if len(buffer) < 20  or self._valid(buffer) == False :
                
                print("[InfraredRemote] Rejected" , len(buffer))
                led.fill((50,0,0));led.write()
                sleep_ms(100)
                led.fill((7,7,0));led.write()
                buffer = []
                continue

            # learnt , save
            print('[InfraredRemote] Learnt {} , length = {}'.format(name,len(buffer)))
            self._store(name,buffer)
            for i in range(0,255,10):
                led.fill((0,i,0));led.write()
                sleep_ms(10)
            for i in range(255,0,-10):
                led.fill((0,i,0));led.write()
                sleep_ms(10)
            led.fill((0,0,0));led.write()
            
            for i in range(3):
                self.send(name)
                sleep_ms(3000)

            core._failsafeActive(True)
            return
            # animation
    def _valid(self,buffer):
        for i in buffer :
            if i < 200 :
                return False
        return True

    def _store(self,name,buffer):
        with open('IR/{}.bin'.format(name),'w') as fp :
            for i in buffer:
                fp.write(str(i))
                fp.write('\n')

    def _load(self,name):
        buffer = []
        with open('IR/{}.bin'.format(name)) as fp :
            for line in fp.readlines():
                buffer.append(int(line))
        return buffer

    def send(self,name):
        buffer = self._load(name)
        isMark = True
        for i in buffer:
            self.pwm.duty(512 if isMark else 0)
            sleep_us(i)
            isMark = not isMark
        self.pwm.duty(0)

