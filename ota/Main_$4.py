ator.rgb.fill((0,0,0));core.indicator.rgb.write();core.time.sleep_ms(50)
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
				core.indicator.rgb.fill((255,0,0));core.indicator.rgb.write