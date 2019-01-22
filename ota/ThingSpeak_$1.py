t()
	bluetooth.send()
	lora.event()
	lora.send()
	
	Module of choice !
	SIM800 , SIM900 , A9G is controverial provide exactly the same count of method
	including 
	sim.getLocation() # gps or gsm
	sim.sendSMS()
	sim.call()
	sim.event()
	sim.socket.send()
	sim.socket.recv()
	sim.socket.event()
	
	
"""