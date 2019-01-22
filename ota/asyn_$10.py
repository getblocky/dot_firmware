return True
		return False

	@classmethod
	def is_running(cls, name):
		return cls._is_running(group=name)

	@classmethod
	def _stopped(cls, task_id):  # On completion remove it
		name = cls._get_group(task_id())  # Convert task_id to task_no
		if name in cls.instances:
			instance = cls.instances[name]
			barrier = instance.barrier
			if barrier is not None:
				barrier.trigger()
			del cls.instances[name]
		Cancellable._stopped(task_id())

	def __init__(self, name, gf, *args, barrier=None, **kwargs):
		if name in self.instances:
			raise ValueError('Task name "{}" already exists.'.format(name))
		super().__init__(gf, *args, group=name, **kwargs)
		self.barrier = barrier
		self.instances[name] = self


# @namedtask
namedtask = cancellable  # compatibility with old code

# Condition class

class Condition():
	def __init__(self, lock=None):
		self.lock = Lock() if lock is None else lock
		self.events = []

	async def acquire(self):
		await self.lock.acquire()

# enable this syntax:
# wi