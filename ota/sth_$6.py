n {}'.format(None if len(r) <= 1 else [r[1],r[2]]))
		return None if len(r) <= 1 else [r[1],r[2]]



# =================== Test Case ======================
a = SIM800()
b = a.socket(2)
async def app():
	await a.gprs(True)
	while True :
		ntp = bytearray(48)
		ntp[0] = 0x1b
		addr = a.getaddrinfo("pool.ntp.org",123)[0][-1]
		res = await b.sendto(ntp,addr)
		msg = await b.recv(48)
		b.close()
		print('MSG = ' , msg)

async def app2():
	while True :
		r = await a.request('+CADC?')
		print('ADC', r)
		await asyncio.sleep_ms(10000)



mainthread.create_task(app())
mainthread.create_task(app2())
start_new_thread(mainthread.run_forever,())
