	"""
		Usage :
			Normally , if the prefix is 'OK' , it will wait for
			this string to show up
				>>> AT
				<<< OK 
			But , sometimes it require data in middle
				>>> AT+CSQ
				<<< +CSQ: 20,0
				<<< OK
				
				-> self.waitingForToken('+CSQ')
				if token is set , the data string will be kept without worrying about \r\nOK
				>>> AT+HTTPREAD
				<<< +HTTPREAD: 5\r\noijfowhf\r\nOKekshk\r\nOK\r\n
				token = +HTTPREAD:5
				message = noijfowhf\r\nOKekshk
				ok = '\r\nOK'
				none = '\r\n'
				
				command will parse this string
				
			But , sometimes , it return OK and data show  up later
				>>> AT+HTTPACTION=0
				<<< OK
				<<< +HTTPACTION: 300
				-> self.waitingForToken('+HTTPACTION')
				-> self.setAsyncAT(True)
				This will tell that the message wont have "OK" and it only return after the token
				show up
				
				
			But , sometimes , thereis un-requested status report , eg :
				>>> SIM Ready
				>>> SMS Ready
				>>> +SMS_ARRIVED
				As this is clearly async at comma