.time.localtime()[4],core.time.localtime()[5])
	if field == "year":
		return core.time.localtime()[0]
	if field == "month":
		return core.time.localtime()[1]
	if field == "date":
		return core.time.localtime()[2]
	if field == "hour":
		return core.time.localtime()[3]
	if field == "minute":
		return core.time.localtime()[4]
	if field == "second":
		return core.time.localtime()[5]
	if field == "day":
		day = core.time.localtime()[6]
		if day == 0 :
			return "Monday"
		if day == 1 :
			return "Tuesday"
		if day == 2 :
			return "Wednesday"
		if day == 3 :
			return "Thursday"
		if day == 4 :
			return "Friday"
		if day == 5 :
			return "Saturday"
		if day == 6 :
			return "Sunday"
	if field.count('/') > 0:
		field = field.replace('dd',str(core.time.localtime()[2]))
		field = field.replace('mm',str(core.time.localtime()[1]))
		field = field.replace('yyyy',str(core.time.localtime()[0]))
		field = field.replace('clock','{}:{}:{}'.format(core.time.localtime()[3],core.time.localtime()[4],core