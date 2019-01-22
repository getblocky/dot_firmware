t self.command('+CIICR')
		await self.request('+CIFSR')
		#await self.command('+CMEE=2')
		#await self.command('+CIFSR;E0',prefix = '11.185.172.8')
		await self.command('+CDNSCFG="203.113.131.1"')
		
		#await self.command('+CIPSSL=1')
		# modemConnect
		#r = await self.command('+CIPSTART=1,"TCP","blynk.getblocky.com",9443',prefix = ["1, CONNECT OK","CONNECT FAIL","ALREADY CONNECT","ERROR","CLOSE OK"])
		r = await self.command('+CIPSTART=1,"UDP","blynk.getblocky.com",80',prefix = ["1, CONNECT OK","CONNECT FAIL","ALREADY CONNECT","ERROR","CLOSE OK"])
		if r == 0 :
			print('[Blynk] Connect successfully !')
ext_socket = SIM800()
sim = ext_socket




mainthread.create_task(main())
mainthread.run_forever()
start_new_thread(mainthread.run_forever,())
		
		
		
			