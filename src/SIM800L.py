"""
	Working Principal
	This library will set the flag on your device
	That tell Blynk to link to this object to send and recv data
	
	WIFI and GPRS is not working simualtanously since these 2 class require lots of memory !
	
	BlynkLib:
		if 'NET_LINK'.flag == True:
			while core.net_link == None :
				await
			self.conn = core.net_link
			
	SIM800L :
		if device.available():
			if eeprom.get('NET_LINK') != True :
				eeprom.set('NET_LINK' , True)
				reset()
			self.init()
			core.net_link = self
		else :
			# Return to WIFI in case this module is not available !
			if eeprom.get('NET_LINK') == True :
				eeprom.set('NET_LINK' , False)
				reset()
			
			If you disconnect this module , please reset the board
			It will not automatically switch to wifi :(
			
			


"""
class SIM800L:
	