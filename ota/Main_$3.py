machine.reset()
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
				core.indic