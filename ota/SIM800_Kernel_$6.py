n(r) <= 1 else [r[1],r[2]]
		
	
	
# =================== Test Case ======================
sim = SIM800()
async def app():
	while True :
		print('='*100)
		r = await sim.request('+CSQ')
		print()
		await sim.gprs(True)
		
		#await sim.http('raw.githubusercontent.com/getblocky/dot_firmware/master/generator.py')
		#await sim.http('cosin.herokuapp.com/test')
		
		await sim.sync_ntp()
		await asyncio.sleep_ms(2000)
async def f1():
	print('SMS is READY')
	
async def event ():
	while True :
		sim.trigger('SMS Ready',f1)
		
		
mainthread.create_task(app())
mainthread.run_forever()
start_new_thread(mainthread.run_forever,())