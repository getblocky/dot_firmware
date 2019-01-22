 , time.ticks_ms() , None , None]
hardware = {"uart" : ['repl',None,None],"spi" : ['flash',None,None]}
async def cleanup():
	print('[CLEANER] -? START')
	global deinit_list , alarm_list
	for x in deinit_list:
		try :
			print('deinit' , x)
			x.deinit()
		except:
			pass
	deinit_list = []	#refresh the list
	alarm_list = [] #delete all alarm stuff
	for x in asyn.NamedTask.instances :
		if x.startswith('user'):
			await asyn.NamedTask.cancel(x)

	a=False
	while a == False :
		a = True
		for x in asyn.NamedTask.instances:
			if x.startswith('user'):
				a = False
				break
		if a == True :
			break
		await asyncio.sleep_ms(10)
	print('[CLEANER] -? DONE')

async def call_once(name,function):
	print('[CALLING] {} -> {}'.format(name,function))
	try :
		if name in asyn.NamedTask.instances:
			if asyn.NamedTask.is_running(name):
				await asyn.NamedTask.cancel ( name )
				while asyn.NamedTask.is_running (name):
					await asyncio.sleep_ms(10)
	except Exception as err:
		del asyn.NamedTask.ins