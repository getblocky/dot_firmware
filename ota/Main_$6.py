
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
				await core.a