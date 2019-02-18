#version=2.0

import sys;core=sys.modules['Blocky.Core']
import machine, time
from machine import Pin

class Distance:
    # echo_timeout_us is based in chip range limit (400cm)
    def __init__(self, port):
        
        self.echo_timeout_us = 500*2*30
        # Init trigger pin (out)
        self.port = port
        self.p = core.getPort(port)

        self.trigger = Pin(self.p[0],Pin.OUT)
        self.trigger.value(0)

        # Init echo pin (in)
        self.echo = Pin(self.p[1],Pin.IN)
        core.deinit_list.append(self)

    def _send_pulse_and_wait(self):
        """
        Send the pulse to trigger and listen on echo pin.
        We use the method `machine.time_pulse_us()` to get the microseconds until the echo is received.
        """
        self.trigger.value(0) # Stabilize the sensor
        time.sleep_us(5)
        self.trigger.value(1)
        # Send a 10us pulse.
        time.sleep_us(10)
        self.trigger.value(0)
        try:
            pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
        except OSError as ex:
            pulse_time = self.echo_timeout_us
        return pulse_time

    def distance_mm(self):
        """
        Get the distance in milimeters without floating point operations.
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.34320 mm/us that is 1mm each 2.91us
        # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582 
        mm = pulse_time * 100 // 582
        return int(mm)

    def distance_cm(self):
        """
        Get the distance in centimeters with floating point operations.
        It returns a float
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.034320 cm/us that is 1cm each 29.1us
        cms = (pulse_time / 2) / 29.1
        return int(cms)

    def getDistance(self,unit='cm'):
        if unit == 'cm':
            return self.distance_cm()
        if unit == 'mm':
            return self.distance_mm()
        else :
            return 0
    
    def deinit(self):
        Pin(self.p[0],Pin.IN)