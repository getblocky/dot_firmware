syncio.sleep_ms(500)
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