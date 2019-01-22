"""
	Footnote 
	:	
		This class utilize internet connection , either wifi or gprs 
		therefore , simply call socket class isnt enough
		Blocky has to wrap this socket class
	:
	
	socket.py
	-> create a socket class 
	
	['__class__', '__init__', '__name__', 'AF_INET', 
	'AF_INET6', 'IPPROTO_IP', 'IPPROTO_TCP', 'IPPROTO_UDP',
	'IP_ADD_MEMBERSHIP', 'SOCK_DGRAM', 'SOCK_RAW', 'SOCK_STREAM', 
	'SOL_SOCKET', 'SO_REUSEADDR', 'getaddrinfo', 'socket']
	
	['__class__', '__name__', 'get', 'put', 'usocket', 'head',
	'Response', 'request', 'post', 'patch', 'delete']
	
	How does this work
	core.socket is a mutable class , which mean either wifi or gprs
	for example , core.socket = gprs
	socket.connect()
	socket.recv()
	although the private class still exist
	gprs.getLocation()
	therefore , core.socket = gprs.socket or sim800.socket
	
	Furthermore , LoRa connection is considering to be hooked !
	No it is not , Lora and Bluetooth is not considered Internet
	It will have seperate block
	
	bluetooth.even