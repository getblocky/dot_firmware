a_data))
			fp.write("\n")
			for x in range(length or len(packet)):
				fp.write(str(packet[x]))
				fp.write("," if x%2==0 else "\n")
		
	def _load(self , name , include_raw = False):
		meta_data = {}
		data = bytearray(1000)
		with open("IR/{}.txt".format(name)) as fp:
			line = fp.readline()
			meta_data = core.json.loads(line)
			
			if not include_raw :
				return meta_data["length"] , meta_data["bin"] , None
			pos = 0
			while line:
				line = fp.readline()
				try :
					data[pos] = (int(line.split(",")[0]))
					pos += 1
				except :
					pass
				try :
					data[pos] =	(int(line.split(",")[1]))
					pos += 1
				except :
					pass
			
			return meta_data["length"] , meta_data["bin"] , data
	
	def _learned(self , name):
		if "{}.txt".format(name) in core.os.listdir("IR"):
			return True
		return False
		
	def _recognise(self , bin):
		for x in self.event_list :
			if self.event_list[x]["bin"] == bin :
				return x
		return None
		
	def _decode(self , packet = None, length = N