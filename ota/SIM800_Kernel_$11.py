s = await socket.sendto(ntp,addr)
		msg = await socket.recv(48)
		await socket.close()
		print('\n\nmsg = ',msg,'\n')
		await asyncio.sleep_ms(5000)

async def csq():
	while True :
		await asyncio.sleep_ms(500)
		state(9,1)
		r = await sim.request('+CSQ')
		state(9,0)

async def cadc():
	while True :
		await asyncio.sleep_ms(500)
		state(5,1)
		r = await sim.request('+CADC?')
		state(5,0)
mainthread.create_task(ntp_application())

start_new_thread(mainthread.run_forever,())
