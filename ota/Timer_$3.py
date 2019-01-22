.time.localtime()[5]))
		return field
		
# Create an alarm at a specific time in a day , hh/mm only. , You can set the second by add another core.wait() command		
async def alarm_service():
	while not core.rtc :
		await core.wait(10000)
		await sync_ntp()
	while True :
		for x in core.alarm_list:
			day , time , function  =  x 
			if core.time.localtime()[6] == day and core.time.localtime()[3] == time[0] \
				and core.time.localtime()[4] == time[1] :
				print("[ALARM] {} {}".format(core.time.localtime() , x))
				core.mainthread.call_soon( core.asyn.Cancellable( function ) () )
				
		
		await core.wait( 60000 - core.time.localtime()[5]*1000)
			
		
def alarm ( day , time , function ):
	day_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
	day = day_list.index(day)
	if day < 0 : 
		return 
	if isinstance(time , str) :
		time = time.split(":")
		time = [int(time[0]) , int(time[1]) ]
	
	print("[ALARM] -> {} {} ".format(day , time) )
	core.alarm_list.appen