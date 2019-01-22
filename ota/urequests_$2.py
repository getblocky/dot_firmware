			await s.write(data)

			l = await  s.readline()
			#print(l)
			l = l.split(None, 2)
			status = int(l[1])
			reason = ""
			if len(l) > 2:
				reason = l[2].rstrip()
			while True:
				l = await s.readline()
				if not l or l == b"\r\n":
					break
				#print(l)
				if l.startswith(b"Transfer-Encoding:"):
					if b"chunked" in l:
						raise ValueError("Unsupported " + l)
				elif l.startswith(b"Location:") and not 200 <= status <= 299:
					raise NotImplementedError("Redirects not yet supported")

		else :
			s.connect(ai[-1])
			if proto == "https:":
				s = ussl.wrap_socket(s, server_hostname=host)
			s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))
			if not "Host" in headers:
				s.write(b"Host: %s\r\n" % host)
			# Iterate over keys to avoid tuple alloc
			for k in headers:
				s.write(k)
				s.write(b": ")
				s.write(headers[k])
				s.write(b"\r\n")
			if json is not None:
				assert data is None
				import ujson
				data = ujson.dumps(json)
				s.write(b"Content-Type: appl