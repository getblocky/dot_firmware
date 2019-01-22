()
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