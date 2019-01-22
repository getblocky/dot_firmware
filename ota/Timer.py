#version=1.0
import sys
core = sys.modules['Blocky.Core']

"""
Main Timer Variable 
[0] :	[Low] Time before feeding
[1]	:	[Important] Timer after feeding ( real time )
[3]	:	NTP at the last sync
[4]	:	Runtime at that sync

Timer Usage :;
	1 . provide runtime function 
	2 . Alarm task using ntp 
	3 . Do not handler any task !
	4 . No task will be execute here , leave it to asyncio
	
"""

core.TimerInfo = [core.time.ticks_ms() , core.time.ticks_ms() , None , None]
# Provide an non-ovf timer count 
def runtime():
	now = core.time.ticks_ms()
	if now < core.TimerInfo[0]:offset =  (1073741823 - core.TimerInfo[1] + now)
	else :	offset =  (now - core.TimerInfo[0])
	core.TimerInfo[1] += offset;core.TimerInfo[0] = now
	return core.TimerInfo[1]
# This function should be call randomly every 10 minutes

	
async def sync_ntp():
	if core.eeprom.get('EXT_RTC') == True :
		return
	else :
		NTP_QUERY = bytearray(48)
		NTP_QUERY[0] = 0x1b
		
		if core.eeprom.get('EXT_SOCKET') == True :
			s = core.ext_so