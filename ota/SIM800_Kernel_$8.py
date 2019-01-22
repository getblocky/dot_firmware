TT="v-internet"')
			await self.command('+CIICR')
			await self.request('+CIFSR',prefix = b'*')

			#await self.command('+CMEE=2')
			#await self.command('+CIFSR;E0',prefix = '11.185.172.8')
			await self.command('+CDNSCFG="203.113.131.1"')
			self.gprs_connected = True
	#============================== SOCKET ===================================#
	def socket(self , *args , **kwargs):
		class socket:
			def __init__(self,super,mode=0):
				self.super = super
				self.id = self.super._liSocket.index(None)
				self.super._liSocket[self.id] = self
				self.sockMode = mode

			async def close(self):
				r = await self.super.command('+CIPCLOSE={},0'.format(self.id),\
					response = [bytes(str(self.id),'utf-8') + b', ' + \
					x for x in [b'CLOSE OK',b'ERROR']]\
				);
				if r == 0:
					self.super._liSocket[self.id] = None
				else :
					raise OSError ('cant close socket')
				return r==0
			async def connect(self,addr):
				while self.super.gprs_connected == False:
					await asyncio.sle