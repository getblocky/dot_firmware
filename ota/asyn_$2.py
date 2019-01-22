rce a coro should issue
# async with lock_instance:
#	access the locked resource

# Alternatively:
# await lock.acquire()
# try:
#   do stuff with locked resource
# finally:
#   lock.release
# Uses normal scheduling on assumption that locks are held briefly.
class Lock():
	
	def __init__(self, delay_ms=0):
		self._locked = False
		self.delay_ms = delay_ms

	def locked(self):
		return self._locked

	async def __aenter__(self):
		await self.acquire()
		return self

	async def __aexit__(self, *args):
		self.release()
		await core.asyncio.sleep(0)

	async def acquire(self):
		while True:
			if self._locked:
				await core.asyncio.sleep_ms(self.delay_ms)
			else:
				self._locked = True
				break

	def release(self):
		if not self._locked:
			raise RuntimeError('Attempt to release a lock which has not been set')
		self._locked = False


# A coro waiting on an event issues await event
# A coro rasing the event issues event.set()
# When all waiting coros have run
# event.clear() should be iss