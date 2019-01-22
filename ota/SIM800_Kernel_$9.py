ep_ms(100)
				#await self.super.command('+CSTT="v-internet"')
				#await self.super.command('+CIICR')
				#await self.super.command('+CIFST',response = [b'*'])
				r = await self.super.command(\
				'+CIPSTART={id},"{mode}","{addr}",{port}'.format(\
				id = self.id,\
				mode = "UDP" if self.sockMode == 2 else "TCP",\
				addr = addr[0],\
				port = addr[1]), \
				response = [bytes(str(self.id),'utf-8') + b', ' + x for x in [b'CONNECT OK',b'ALREADY CONNECT',b'CONNECT FAIL'] ],\
				timeout = 10000);return False if r == 2 else True
			async def recv(self,length):
				await self.super.waitfor('+CIPRXGET: 1,{id}'.format(id=self.id),timeout = 5000)
				r = await self.super.request('+CIPRXGET=2,{id},{length}'.format(id=self.id,length=length),	prefix = b'**')
				# r = [RECEIVED,PENDING]
				parsed = 0;_string = b''
				_string = r[0]
				if len(_string) < length :
					_string += self.buffer[0:(length - len(_string))]
					self.buffer = self.buffer[0:(length-len(_string))]

				return r
