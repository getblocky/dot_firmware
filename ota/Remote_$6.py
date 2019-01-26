machine.Pin.IN)
		core.time.sleep_ms(5)

	def _store(self , name , packet , bin , length = None):
		meta_data = {"bin":bin , "length": length or len(packet) , "protocol" : "RAW"}
		with open("IR/{}.txt".format(name),"w") as fp :
			fp.write(core.json.dumps(meta_data))
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
		if "{}.