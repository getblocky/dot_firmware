w):
	return await request("PUT", url, **kw)

async def patch(url, **kw):
	return await request("PATCH", url, **kw)

async def delete(url, **kw):
	return await request("DELETE", url, **kw)
