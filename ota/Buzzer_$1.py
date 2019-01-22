f isinstance(sequence,list):
				if len(sequence) % 2 == 0:
					self.pwm.duty(duty or 100)
					for x in range(0,len(sequence),2):
						if sequence[x] != 0 :
							self.pwm.freq(sequence[x])
						else :
							self.pwm.duty(0)
						await core.wait(sequence[x+1])
						self.pwm.duty(0)
						await core.wait(gap)
						self.pwm.duty(duty or 100)
					self.pwm.duty(0)
		except (TypeError,ValueError) as err :
			import sys
			sys.print_exception(err)

	def deinit(self):
		self.pwm.deinit()
		Pin(self.p[0],Pin.IN)
