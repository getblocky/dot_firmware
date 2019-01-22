ication/json\r\n")
			if data:
				s.write(b"Content-Length: %d\r\n" % len(data))
			s.write(b"\r\n")
			if data:
				s.write(data)

			l = s.readline()
			#print(l)
			l = l.split(None, 2)
			status = int(l[1])
			reason = ""
			if len(l) > 2:
				reason = l[2].rstrip()
			while True:
				l = s.readline()
				if not l or l == b"\r\n":
					break
				#print(l)
				if l.startswith(b"Transfer-Encoding:"):
					if b"chunked" in l:
						raise ValueError("Unsupported " + l)
				elif l.startswith(b"Location:") and not 200 <= status <= 299:
					raise NotImplementedError("Redirects not yet supported")
	except OSError:
		if ext == True :
			await s.close()
		else :
			s.close()
		raise

	resp = Response(s)
	resp.status_code = status
	resp.reason = reason
	return resp


async def head(url, **kw):
	return await request("HEAD", url, **kw)

async def get(url, **kw):
	return await request("GET", url, **kw)

async def post(url, **kw):
	return await request("POST", url, **kw)

async def put(url, **k