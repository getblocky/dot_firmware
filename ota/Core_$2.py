library_version(lib):
	if '{}.py'.format(lib) not in os.listdir('Blocky'):
		return None
	line = ''
	f = open('Blocky/{}.py'.format(lib))
	while True :
		temp = f.read(1)
		if len(temp) == 0 or temp == '\n' or temp == '\r':
			break
		line += temp
	# #version=1.0
	if not line.startswith('#version'):
		f.close()
		return 0.0
	f.close()
	return float(line.split('=')[1])
	
"""
	Patch function , do not use await core.asyncio.sleep_ms(time) with time > 5s , this will block OTA process
	since it need to wait for the _sleep_ms task to be done.
	
	core.asyncio.sleep_ms(time)  ->  core.wait(time)  #ms
"""
async def wait ( time ):
	for x in range( time//500):
		await asyncio.sleep_ms(500)
	await asyncio.sleep_ms(time % 500)
	
_failsafe = None
def _failsafeActive(state):
	if state == True :
		try :
			core.wdt_timer.init(mode=core.machine.Timer.PERIODIC,period=20000,callback = _failsafe)
		except :
			pass
	if state == False :
		try :
			core.wdt_timer.deinit()
		except :
			pass
