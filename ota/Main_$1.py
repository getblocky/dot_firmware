rint('[user-code] -> run directly')
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
		core.machine.reset()
	
async def send_last_word():





	if "last_word.py" in core.os.listdir():
		while core.blynk.state != 3 :
			await core.wait(200)
		try :
			print('[lastword] -> {}'.format(open('last_word.py').read()),end = '')
			await core.blynk.log(open('last_word.py').read())
