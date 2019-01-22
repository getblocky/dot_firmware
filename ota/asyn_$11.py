th await condition [as cond]:
	def __await__(self):
		yield from self.lock.acquire()
		return self

	__iter__ = __await__

	def __enter__(self):
		return self

	def __exit__(self, *_):
		self.lock.release()

	def locked(self):
		return self.lock.locked()

	def release(self):
		self.lock.release()  # Will raise RuntimeError if not locked

	def notify(self, n=1):  # Caller controls lock
		if not self.lock.locked():
			raise RuntimeError('Condition notify with lock not acquired.')
		for _ in range(min(n, len(self.events))):
			ev = self.events.pop()
			ev.set()

	def notify_all(self):
		self.notify(len(self.events))

	async def wait(self):
		if not self.lock.locked():
			raise RuntimeError('Condition wait with lock not acquired.')
		ev = Event()
		self.events.append(ev)
		self.lock.release()
		await ev
		await self.lock.acquire()
		assert ev not in self.events, 'condition wait assertion fail'
		return True  # CPython compatibility

	async def wait_for(self, predicate):
		result = predicat