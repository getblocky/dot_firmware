import sys
core = sys.modules['Blocky.Core']

class EEPROM :
	def __init__(self,file='eeprom'):
		self.file = file
		if not self.file in core.os.listdir():
			f = open(self.file,'w')
			f.close()
		self.data = {}
		try :
			self.data = core.json.loads(open(self.file).read())
		except :
			pass
	def get(self,name):
		try :
			value = self.data[name]
			return value
		except KeyError:
			return None
		
	def set(self,name,value):
		try :
			if self.data[name] == value:
				return False
		except KeyError:
			pass
		self.data[name] = value
		f = open(self.file,'w')
		f.write(core.json.dumps(self.data))
		f.close()
		return True
