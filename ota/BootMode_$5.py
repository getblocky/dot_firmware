en(id), 2)]

		max_index = 0 ; max_value = 0
		for x in range(6):
		  if int(uuid[x],16) > max_value:
			max_value = int(uuid[x],16)
			max_index = x
			
		# Try to make an color indicator for which is which 
		# Blocky that shine red will be 'Blocky RED <uuid>'
		color = []
		n=5
		if max_index == 0 : color = ['red',	(255//n,0//n,0//n)]
		if max_index == 1 : color = ['green',	(0//n,255//n,0//n)]
		if max_index == 2 : color = ['blue',	(0//n,0//n,255//n)]
		if max_index == 3 : color = ['white',(50//n,50//n,50//n)]
		if max_index == 4 : color = ['purple',(100//n,0//n,100//n)]
		if max_index == 5 : color = ['yellow', (100//n,100//n,0//n)]
		
		core.indicator.rgb.fill(color[1]);core.indicator.rgb.write()
		core.mainthread.create_task(core.indicator.heartbeat( color[1] , 1 ,core.flag.wifi , 5) )
		ap_name = 'Blocky ' + color[0].upper() +' '+ core.binascii.hexlify(core.machine.unique_id()).decode('ascii')[0:4]
	
		print(ap_name)
		
		
		ap_password = ''
		wifi_status = 0
		
		
		#-----------