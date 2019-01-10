
			await asyncio.sleep_ms(1)
		





async def ota ():
	print('[Blynk] OTA Process Begin')
	
async def main():
	#blynk = Blynk('e5e5e772d112462c8c29462289cf0f1c',server = 'blynk.getblocky.com',ota=ota)
	blynk = Blynk('e80ff069a180413cb357e059bb0a1568',server = 'blynk.getblocky.com',ota=ota)
	mainthread.create_task(blynk.run())


mainthread.create_task(main())
mainthread.run_forever()
start_new_thread(mainthread.run_forever,())
		
		
		
			