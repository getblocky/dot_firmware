t(500)
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
		core.