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
	if core.Timer.runtime() > 60000 and core.eeprom.get('EXT_SOCKET') == True and core.ext_socket == None :
		core.eeprom.set('EXT_SOCKET',False)
		core.os.rename('user_code.py','temp.py')
		open('last_word.py','w').write('[HARDWARE] socket not found')
		core.machine.reset()
	if core.Timer.runtime() - core.blynk.last_call > 20000 :
		if core.eeprom.get('EXT_SOCKET') == True :
			return
		else :
			if not core.wifi.wlan_sta.isconnected():
				print('[failsafe] -> wifi is so bad')
		