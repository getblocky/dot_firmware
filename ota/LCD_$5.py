int):
				if line <= self.line :
					self.lcd.move_to(0,line-1)
					self.lcd.putstr(' '*self.column)
		except Exception :
			self.reinit = True
			pass
	def display(self,line = 0 , left = '' , right = ''):
		try :
			if self.reinit == True :
				self.lcd.init()
				self.reinit = False
			if line <= self.line :
				self.lcd.move_to(0,line-1)
				right = str(right)
				left = str(left)

				if len(right) > 0:
					left =left[0:self.column-len(right)-1]
					string = left +':' + ' '*(self.column-len(left)-len(right)-1)+ right
				else :
					string = left + ' '*(self.column-len(left))

				if len(string) > self.column :
					string = string[0:self.column]
				self.lcd.putstr(string)
		except Exception :
			self.reinit = True
			pass

	def backlight(self , state = 'on'):
		try :
			if self.reinit == True :
				self.lcd.init()
				self.reinit = False
			if state == 'on' :
				self.lcd.backlight_on()
			if state == 'off' :
				self.lcd.backlight_off()
		except Exception:
			self.reinit = T