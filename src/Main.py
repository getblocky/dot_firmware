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
		for x in core.deinit_list:
			try :
				x.deinit()
			except :
				pass
		core.machine.reset()
core._failsafe = _failsafe

async def run_user_code(direct = False):
	"""
		Pending library that need to be download will be downloaded first , it will yield back
	"""
	print('run user code = True')
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
		print('[user-code] -> run directly')
		core._failsafeActive(True)
		core.user_code = __import__('user_code')
		core.gc.collect()
		await core.blynk.log('[HEAP] {}'.format(core.gc.mem_free())  )
		return

	list_library = core.get_list_library('user_code.py')
	list_library_update = []
	for x in list_library:
		print('[library] -> checking {}'.format(x) , end = '')
		current_version = core.get_library_version(x[0])
		if current_version == None or current_version < x[1] :
			list_library_update.append(x[0])
			print(False)
		else :
			print(True)

	if len(list_library_update):
		core.eeprom.set('LIB',list_library_update)
		core.machine.reset()
	core._failsafeActive(True)
	try :
		del core.sys.modules['user_code']
	except :
		pass
	core.gc.collect()
	print('[user_code] -> started with {} heap'.format(core.gc.mem_free()))
	try :
		core.user_code = __import__('user_code')
		core.gc.collect()
		await core.blynk.log('[HEAP] {}'.format(core.gc.mem_free()) )
	except RuntimeError:
		del core.sys.modules['user_code']
		while not core.wifi.wlan_sta.isconnected() or core.flag.blynk == False:
			await core.asyncio.sleep_ms(500)
		core.mainthread.create_task(run_user_code(True))
		return
	except MemoryError as err:
		if not core.flag.direct_command:
			del core.sys.modules['user_code']
			print('[memory] -> removing user code')
			try :
				core.os.rename('user_code.py','temp_code.py')
			except :
				pass
			f = open('last_word.py','w')
			f.write('[DOT_ERROR] MEMORY {}'.format(err))
			f.close()
			for x in range(20):
				core.indicator.rgb.fill((255,0,0));core.indicator.rgb.write();core.time.sleep_ms(50)
				core.indicator.rgb.fill((0,0,0));core.indicator.rgb.write();core.time.sleep_ms(50)
		for x in core.deinit_list:
			try:
				x.deinit()
			except:
				pass
		core.machine.reset()

async def send_last_word():





	if "last_word.py" in core.os.listdir():
		while core.blynk.state != 3 :
			await core.wait(200)
		try :
			print('[lastword] -> {}'.format(open('last_word.py').read()),end = '')
			await core.blynk.log(open('last_word.py').read())
		except :
			pass
		finally :
			core.os.remove('last_word.py')

async def main(online=False):
	if not core.cfn_btn.value():
		time = core.time.ticks_ms()
		print('Configure: ',end='')
		while not core.cfn_btn.value():
			core.time.sleep_ms(500)
			temp = ( core.time.ticks_ms() - time ) //1000
			if temp > 0 and temp < 3 :
				core.indicator.rgb.fill((0,25,0));core.indicator.rgb.write()
			if temp > 3 and temp < 6 :
				core.indicator.rgb.fill((25,25,0));core.indicator.rgb.write()
			if temp > 6:
				core.indicator.rgb.fill((255,0,0));core.indicator.rgb.write()
		time = core.time.ticks_ms() - time ; time = time//1000
		if time > 0 and time < 3 :
			from Blocky.BootMode import BootMode
			bootmode = BootMode()
			await bootmode.Start()
		if time > 3 and time < 6 :
			core.os.remove('user_code.py')
			core.os.remove('eeprom')
		if time > 6 :
			core.os.remove('user_code.py')
			core.os.remove('config.json')
			core.os.remove('eeprom')
			try :
				core.os.remove('Blocky/fuse.py')
			except:
				pass
		core.machine.reset()

	#
	try :
		core.config = core.json.loads(open('config.json').read())
		if not all(elem in list(core.config.keys()) for elem in ['token','known_networks']):
			raise Exception
		if len(core.config['token']) == 0 or len(core.config['known_networks'])==0:
			raise Exception

	except Exception as err:
		core.sys.print_exception(err)
		print('[config] -> error , init bootmode')
		from Blocky.BootMode import BootMode
		bootmode = BootMode()
		await bootmode.Start()
		core.machine.reset()


	core.wifi = __import__('Blocky/wifi')
	from Blocky.BlynkLib import Blynk

	print('[main] connecting via external device')
	core.mainthread.create_task(run_user_code())
	core.mainthread.create_task(send_last_word())
	core.mainthread.create_task(core.Timer.alarm_service())

	core.blynk = Blynk(core.config['token'],ota = run_user_code)

	# await for network , then download new file
	while True :
		if core.eeprom.get('EXT_SOCKET') == True : # running on external device
			# await network object to be loaded
			while core.ext_socket == None :
				await core.asyncio.sleep_ms(200)
			# await that network connection
			while not core.ext_socket.isconnected() :
				await core.asyncio.sleep_ms(200)


		else : # running on wifi
			if not core.wifi.wlan_sta.isconnected():
				print('[wifi] connecting back')
				await core.wifi.connect(core.config['known_networks'])

		if core.flag.blynk == False :
			print('[blynk] -> connecting back now')
			core.mainthread.create_task(core.blynk.run())
			while not core.flag.blynk:
				await core.asyncio.sleep_ms(500)
			print('[blynk] -> back online')

		if core.eeprom.get('LIB') != None:
			print('[library] downloading {}'.format(core.eeprom.get('LIB')))
			for x in core.eeprom.get('LIB'):
				core.download(x+'.py','Blocky/{}.py'.format(x))
			core.eeprom.set('LIB',None)
			core.mainthread.create_task(run_user_code(True))

		while not core.flag.blynk:
			await core.asyncio.sleep_ms(500)
		print('You are back online :) Happy Blynking')
		core.blynk.log('[DOT_ONLINE]\t{}\t{}\t{}'.format(core.Timer.current('clock'),core.wifi_list,core.wifi.wlan_sta.config('essid')))
		while core.flag.blynk :
			await core.asyncio.sleep_ms(1000)
def wrapper():
	while True :
		try :
			core.mainthread.run_forever()
		except MemoryError as err:
			if not core.flag.direct_command:
				f = open('last_word.py','w')
				f.write('[DOT_ERROR] {}'.format(str(err)))
				f.close()
				core.os.rename('user_code.py', 'temp_code.py')
			for x in core.deinit_list:
				try :
					x.deinit()
				except :
					pass
			core.machine.reset()
		except Exception as err :
			core.sys.print_exception(err)
			core.time.sleep_ms(1000)
			core.mainthread.call_soon(core.blynk.log('[DOT_ERROR] {}'.format(str(err))))

core.blynk = None
core.mainthread.create_task(main())
wrapper()
#core._thread.start_new_thread(wrapper,())
