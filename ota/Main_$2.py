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
		if time > 6 :
			core.os.remove('user_code.py')
			core.os.remove('config.json')
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
		
	# when in Offline mode , press config to be back online
	if core.eeprom.get('OFFLINE') == True  :
		def back_online(s):
			core.mainthread.call_soon(main(True))
			core.cfn_btn.irq(trigger=0)
		core.cfn_btn.irq(trigger = core.machine.Pin.IRQ_FALLING , handler = back_online)
		print('running offline mode ! press config to be back online')
		if core.eeprom.get('EXT_SOCKET') == True :
			print('[OFFLINE MODE] -> running blynk , timer and other service')
			core.blynk = Blynk(core.config['token'],ota = run_user_code)
		