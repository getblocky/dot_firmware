 content))

	async def virtual_write(self,pin,val,device = None):
		if self.state == AUTHENTICATED:
			if device == None:
				await self._send(self._format_msg(MSG_HW, 'vw', pin, val))
			else :
				await self._send(self._format_msg(MSG_BRIDGE ,124, 'i' , device)) # Set channel V124 of this node to point to that device
				await self._send(self._format_msg(MSG_BRIDGE, 124,'vw',  pin , val))

	async def set_property(self, pin, prop, val):
		if self.state == AUTHENTICATED:
			await self._send(self._format_msg(MSG_PROPERTY, pin, prop, val))

	async def log_event(self, event, descr=None):
		if self.state == AUTHENTICATED:
			if descr==None:
				await self._send(self._format_msg(MSG_EVENT_LOG, event))
			else:
				await self._send(self._format_msg(MSG_EVENT_LOG, event, descr))

	async def log(self,message):
		await self.virtual_write(device = self._token.decode('utf-8') , pin = 127 , val = message )
		#await self.virtual_write( pin = 127 , val = message )

	async def sync_all(self):
		if se