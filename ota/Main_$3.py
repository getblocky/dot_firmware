	core.mainthread.create_task(send_last_word())
			core.mainthread.create_task(core.Timer.alarm_service())
		print('[OFFLINE MODE] -> initialize user_code')
		core.user_code = __import__('user_code')
		
		return
	
	
	print('[wifi] -> connecting')
	core.wifi = __import__('Blocky/wifi')
	from Blocky.BlynkLib import Blynk
	core.blynk = Blynk(core.config['token'],ota = run_user_code)
	core.mainthread.create_task(send_last_word())
	core.mainthread.create_task(run_user_code())
	core.mainthread.create_task(core.Timer.alarm_service())
	while True :
		await core.asyncio.sleep_ms(500)
		if not core.wifi.wlan_sta.isconnected():
			print('[wifi] -> connecting back',end='')
			await core.wifi.connect(core.config['known_networks'])
			print('OK')
			if core.eeprom.get('LIB')!= None:
				print('[library] -> downloading list {}'.format(core.eeprom.get('LIB')))
				for x in core.eeprom.get('LIB'):
					core.download(x+'.py','Blocky/{}.py'.format(x))
				core.eeprom.set('LIB',None)
				core.mainthread.create_task(run_user_code(True))
			print('[blynk] -> connecting back')
			core.mainthread.create_task(core.blynk.run())
			while not core.flag.blynk:
				await core.asyncio.sleep_ms(500)
			print('You are back online :) Happy Blynking')
			core.blynk.log('[DOT_ONLINE]\t{}\t{}\t{}'.format(core.Timer.current('clock'),core.wifi_list,core.wifi.wlan_sta.config('essid')))
		if core.flag.blynk == False :
			print('[blynk] -> connecting back now')
			core.mainthread.create_task(core.blynk.run())
			while not core.flag.blynk:
				await core.asyncio.sleep_ms(500)
			print('[blynk] -> back online')

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
			core.machine.reset()
		except Exception as err :
			core.sys.print_exception(err)
			core.time.sleep_ms(1000)
			core.main