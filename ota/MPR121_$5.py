touched()
		return (t & (1 << electrode)) != 0
		
	def event ( self , type , pin , function ):
		self.handler[pin][0 if type=='touch' else 1] = function
	
	@core.asyn.cancellable
	async def poller (self):
		while True :
			if self.error == True :
				self.reset()
			try :
				now = self.touched()
				if now != self.prev :
					for x in range(11):
						if get_bit(self.prev,x) != get_bit(now,x):
							if get_bit(now , x):
								if self.handler[x][0] != None :
									if core.flag.duplicate == True :
										core.mainthread.call_soon ( core.asyn.Cancellable( self.handler[x][0] )() )
									else :
										await core.call_once('user_mpr121_{}_{}_{}'.format(self.port , x,1),self.handler[x][0])
							else :
								if self.handler[x][1] != None :
									if core.flag.duplicate == True :
										core.mainthread.call_soon ( core.asyn.Cancellable( self.handler[x][1] )() )
									else :
										await core.call_once('user_mpr121_{}_{}_{}'.format(self.port , x,0),self.handler[x][