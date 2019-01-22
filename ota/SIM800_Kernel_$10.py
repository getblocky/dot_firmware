			async def sendto(self,data,addr):
				await self.connect( addr)
				await self.write( data )

			async def write(self , data , length = None):
				r = await self.super.command('+CIPSEND={id},{length}'.format(id = self.id , length = len(data) if length == None else data[:length]),\
					response = [b'> '])
				if not isinstance(data,bytes):
					try :
						if isinstance(data,str):
							data = bytes(data,'utf-8')
						elif isinstance(data,bytearray):
							data = bytes(data)
					except TypeError as error:
						import sys
						sys.print_exception(error)
						if self.debug :
							print('[ERROR] Can not convert to bytes')
							print('BUF = ',data)

				r = await self.super.request(data , prefix = b'DATA ACCEPT:{},'.format(self.id))

		new_socket = socket(self , *args,**kwargs)
		return new_socket


sim = SIM800()

async def ntp_application():
	while True :
		ntp = bytearray(48)
		ntp[0] = 0x1b
		addr = sim.getaddrinfo('pool.ntp.org',123)[0][-1]

		socket = sim.socket(2)
		re