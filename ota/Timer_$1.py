cket.socket(core.ext_socket.AF_INET,core.ext_socket.SOCK_DGRAM)
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