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
			await core.wai