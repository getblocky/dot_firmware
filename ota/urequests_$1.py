"/", 3)
	except ValueError:
		proto, dummy, host = url.split("/", 2)
		path = ""
	if proto == "http:":
		port = 80
	elif proto == "https:":
		if ext != True :
			import ussl
		port = 443
	else:
		raise ValueError("Unsupported protocol: " + proto)

	if ":" in host:
		host, port = host.split(":", 1)
		port = int(port)

	ai = usocket.getaddrinfo(host, port, 0, usocket.SOCK_STREAM)
	ai = ai[0]

	s = usocket.socket(ai[0], ai[1], ai[2])
	try:
		if ext  == True :
			await s.connect(ai[-1])
			await s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))
			if not "Host" in headers:
				await s.write(b"Host: %s\r\n" % host)
			for k in headers:
				await s.write(k)
				await s.write(b": ")
				await s.write(headers[k])
				await s.write(b"\r\n")
			if json is not None:
				assert data is None
				import ujson
				data = ujson.dumps(json)
				await s.write(b"Content-Type: application/json\r\n")
			if data:
				await s.write(b"Content-Length: %d\r\n" % len(data))
			await s.write(b"\r\n")
			if data:
	