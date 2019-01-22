0):
				self.super = super
				self.id = self.super._liSocket.index(None)
				self.super._liSocket[self.id] = self


				self.sockMode= mode # 2 if UDP , 0 if TCP



			async def close(self):
				r = await self.super.command('+CIPCLOSE={},0'.format(self.id),\
					response = [bytes(str(self.id),'utf-8') + b', ' + \
					x for x in [b'CLOSE OK',b'ERROR']]\
				);return r==0

			async def connect(self,addr):
				#await self.super.command('+CSTT="v-internet"')
				#await self.super.command('+CIICR')
				#await self.super.command('+CIFST',response = [b'*'])
				r = await self.super.command(\
					'+CIPSTART={id},"{mode}","{addr}",{port}'.format(\
						id = self.id,\
						mode = "UDP" if self.sockMode == 2 else "TCP",\
						addr = addr[0],\
						port = addr[1]), \
					response = [bytes(str(self.id),'utf-8') + b', ' + x for x in [b'CONNECT OK',b'ALREADY CONNECT',b'CONNECT FAIL'] ]\
				);return False if r == 2 else True
			async def recv(self,length):
				await self.super.waitfor('+CIPR