ore.time.sleep_us
		self.recv.irq(trigger = 0,handler = None)
		sleep(1000)
		for x in range(length):
			duty(512 if x%2==0 else 0)
			sleep(packet[x]*50)
		duty(0)
		sleep(3000)
		self._recvActive(True)

	async def get_learned(self):
		print('[REMOTE_LEARNED] {}'.format([x.split('.')[0] for x in core.os.listdir('IR')]))
		while core.flag.blynk == False :
			await core.wait(200
		await core.blynk.log(
