ubclass
		Cancellable.task_no += 1
		self.task = task

	def __call__(self):
		return self.task

	def __await__(self):  # Return any value returned by task.
		return (yield from self.task)

	__iter__ = __await__


# @cancellable decorator

def cancellable(f):
	
	def new_gen(*args, **kwargs):
		if isinstance(args[0], TaskId):  # Not a bound method
			task_id = args[0]
			g = f(*args[1:], **kwargs)
		else:  # Task ID is args[1] if a bound method
			task_id = args[1]
			args = (args[0],) + args[2:]
			g = f(*args, **kwargs)
		try:
			res = await g
			return res
		finally:
			NamedTask._stopped(task_id)
	return new_gen

# The NamedTask class enables a coro to be identified by a user defined name.
# It constrains Cancellable to allow groups of one coro only.
# It maintains a dict of barriers indexed by name.
class NamedTask(Cancellable):
	instances = {}

	@classmethod
	async def cancel(cls, name, nowait=True):
		if name in cls.instances:
			await cls.cancel_all(group=name, nowait=nowait)
			