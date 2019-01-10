"""
MicroPython TinyRTC I2C Module, DS1307 RTC + AT24C32N EEPROM
https://github.com/mcauser/micropython-tinyrtc

MIT License
Copyright (c) 2018 Mike Causer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

BCD Format:
https://en.wikipedia.org/wiki/Binary-coded_decimal
"""


"""
	DS1307.py
		In combination with NTP !
		
		if self.available():
			if core.rtc == None :
				core.rtc = self.getTime()
			else :
				return
		
		# Sync time from NTP to DS1307 !
	
	Timer.py NTP.py
	
	if eeprom.get('RTC_DEVICE') == True :
		while core.rtc_device == None :
			await
		try :
			current_time = get_ntp()
			core.rtc_device.set_time(current_time)
			core.rtc.set_time(current_time)
		except :
			# No internet conditions
			core.rtc.set_time(core.rtc_device.getTime())
			pass

"""
from micropython import const

DATETIME_REG = const(0) # 0x00-0x06
CHIP_HALT    = const(128)
CONTROL_REG  = const(7) # 0x07
RAM_REG      = const(8) # 0x08-0x3F

class DS1307(object):
    """Driver for the DS1307 RTC."""
    def __init__(self, i2c, add