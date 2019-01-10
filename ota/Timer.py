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
			s = core.ext_socket.socket(core.ext_socket.AF_INET,core.ext_socket.SOCK_DGRAM)
			await s.settimeout(1)
			res = await s.sendto(NTP_QUERY,["pool.ntp.org",123])
			msg = await s.recv(48)
			await s.close()
		else :
			if core.wifi.wlan_sta.isconnected():
				addr = core.socket.getaddrinfo("pool.ntp.org", 123)[0][-1]
				s = core.socket.socket(core.socket.AF_INET, core.socket.SOCK_DGRAM)
				s.settimeout(1)
				res = s.sendto(NTP_QUERY, addr)
				msg = s.recv(48)
				s.close()
			else :
				return
				
		val = core.struct.unpack("!I", msg[40:44])[0]
		t = val - 3155673600
		gmt = core.eeprom.get('GMT')
		if gmt != None :
			t += gmt * 3600
		tm = core.time.localtime(t)
		tm = tm[0:3] + (0,) + tm[3:6] + (0,)
		core.machine.RTC().datetime(tm)
		print('[NTP] Synced at {}'.format(core.time.localtime()))
		core.rtc = True
		
def current(field=None):
	if core.rtc == False :
		return 
	if field==None:
		return core.time.localtime()
	if field == "clock":
		return '{}:{}:{}'.format(core.time.localtime()[3],core