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
            pulse_time = machine.