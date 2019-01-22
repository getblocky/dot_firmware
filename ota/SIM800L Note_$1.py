r finish , it return a +httpaction flag
	the function that require this must wait for this flag to be set
	this flag will be set by the rountine , therefore , there are offtime
	
	for others task like http read
	sim800 return the string immediately , what if inside the content we have "OK" :)
	example 
		>>> AT+HTTPREAD
		<<< +HTTPREAD :8
		<<< hello OK
		<<< OK
	with this one , the routine must be a bit smarter to realize that 8 bytes is data !
	
	
	
	
In Conjunction with common funciton :
	there are 2 kind of operation 
		AaA ( ask and answer ):
			this operation will set the flag preventi
			
		Event -> __routine__
			exitCondition = any() = 1 and buf.endswith('OK\r\n')
			
	
	
	
	
	
	
	
	
	
	
	