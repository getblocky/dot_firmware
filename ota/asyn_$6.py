Semaphore(Semaphore):
	
	def __init__(self, value=1):
		super().__init__(value)
		self._initial_value = value

	def release(self):
		if self._count < self._initial_value:
			self._count += 1
		else:
			raise ValueError('Semaphore released more than acquired')
"""
# Task Cancellation
try:
	StopTask = core.asyncio.CancelledError  # More descriptive name
except AttributeError:
	raise OSError('asyn.py requires ucore.asyncio V1.7.1 or above.')
"""
class TaskId():
	
	def __init__(self, taskid):
		self.taskid = taskid

	def __call__(self):
		return self.taskid

# Sleep coro breaks up a sleep into shorter intervals to ensure a rapid
# response to StopTask exceptions
async def sleep(t, granularity=100):  # 100ms default
	
	if granularity <= 0:
		raise ValueError('sleep granularity must be > 0')
	t = int(t * 1000)  # ms
	if t <= granularity:
		await core.asyncio.sleep_ms(t)
	else:
		n, rem = divmod(t, granularity)
		for _ in range(n):
			await core.asyncio.sleep_ms(granularity)
		await core.asyn