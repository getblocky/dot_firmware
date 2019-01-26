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
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self.weekday_start = 1
        self._halt = False

    def _dec2bcd(self, value):
        """Convert decimal to binary coded decimal (BCD) format"""
        return (value // 10) << 4 | (value % 10)

    def _bcd2dec(self, value):
        """Convert binary coded decimal (BCD) format to decimal"""
        return ((value >> 4) * 10) + (value & 0x0F)

    def datetime(self, datetime=None):
        """Get or set datetime"""
        if datetime is None:
            buf = self.i2c.readfrom_mem(self.addr, DATETIME_REG, 7)
            return (
                self._bcd2dec(buf[6]) + 2000, # year
                self._bcd2dec(buf[5]), # month
                self._bcd2dec(buf[4]), # day
                self._bcd2dec(buf[3] - self.weekday_start), # weekday
                self._bcd2dec(buf[2]), # hour
                self._bcd2dec(buf[1]), # minute
                self._bcd2dec(buf[0] & 0x7F), # second
                0 # subseconds
            )
        buf = bytearray(7)
        buf[0] = self._dec2bcd(datetime[6]) & 0x7F # second, msb = CH, 1=halt, 0=go
        buf[1] = self._dec2bcd(datetime[5]) # minute
        buf[2] = self._dec2bcd(datetime[4]) # hour
        buf[3] = self._dec2bcd(datetime[3] + self.weekday_start) # weekday
        buf[4] = self._dec2bcd(datetime[2]) # day
        buf[5] = self._dec2bcd(datetime[1]) # month
        buf[6] = self._dec2bcd(datetime[0] - 2000) # year
        if (self._halt):
            buf[0] |= (1 << 7)
        self.i2c.writeto_mem(self.addr, DATETIME_REG, buf)
