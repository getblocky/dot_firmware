#version=2.0
import Blocky.Core as core
from Blocky.Indicator import indicator
core.indicator = indicator
core.mainthread = core.asyncio.get_event_loop()
core.gc.threshold(90000)
if 'user_code.py' not in core.os.listdir():
	f = open('user_code.py','w')
	f.close()
if 'temp_code.py' not in core.os.listdir():
	f = open('temp_code.py','w')
	f.close()
if 'config.json' not in core.os.listdir():
	f = open('config.json','w')
	f.close()
try :
	core.wdt_timer = core.machine.Timer(1)
except :
	pass	

def _failsafe(source):
	if core.Timer.runtime() - core.blynk.last_call > 20000 :
		if core.eeprom.get('EXT_SOCKET') == True :
			return
		else :
			if not core.wifi.wlan_sta.isconnected():
				print('[failsafe] -> wifi is so bad')
				return
				
		if not core.flag.direct_command:
			import os , machine,time
			print('[failsafe] -> removing user code')
			try :
				core.os.rename('user_code.py','temp_code.py')
			except :
				pass
			f = open('last_word.py','w')
			f.write('[DOT_ERROR] BLOCKING')
			f.close()
			for x in range(20):
				core.indicator.rgb.fill((255,0,0));core.indicator.rgb.write();time.sleep_ms(50)
				core.indicator.rgb.fill((0,0,0));core.indicator.rgb.write();time.sleep_ms(50)
		f = open('last_word.py','w')
		f.write('[DOT_ERROR] BLOCKING_CMD')
		f.close()
		core.machine.reset()
core._failsafe = _failsafe

async def run_user_code(direct = False):
	"""
		Pending library that need to be download will be downloaded first , it will yield back
	"""
	if direct == False and core.eeprom.get('LIB') != None :
		return 
	if core.os.stat('user_code.py')[6] == 0 :
		while not core.flag.blynk :
			await core.wait(500)
		await core.indicator.rainbow()
		return
	else :
		await core.indicator.show(None)
	core._failsafeActive(False)
	
	""" 
		By defaults , the system will run user code and connecting at the same time
		Sometimes , these two task yield RuntimeError 
		Which will kill user code , wait for the network to connect and then re-run user_code
	"""
	if direct == True :
		p