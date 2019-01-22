asks = cls._get_task_nos(group)
		if tasks == []:
			return False
		for task_no in tasks:
			barrier = cls.tasks[task_no][2]
			if barrier is None:  # Running, not yet cancelled
				return True
			if barrier.busy():
				return True
		return False

	@classmethod
	def _get_task_nos(cls, group):  # Return task nos in a group
		return [task_no for task_no in cls.tasks if cls.tasks[task_no][1] == group]

	@classmethod
	def _get_group(cls, task_no):  # Return group given a task_no
		return cls.tasks[task_no][1]

	@classmethod
	def _stopped(cls, task_no):
		if task_no in cls.tasks:
			barrier = cls.tasks[task_no][2]
			if barrier is not None:  # Cancellation in progress
				barrier.trigger()
			del cls.tasks[task_no]

	def __init__(self, gf, *args, group=0, **kwargs):
		task = gf(TaskId(Cancellable.task_no), *args, **kwargs)
		if task in self.tasks:
			raise ValueError('Task already exists.')
		self.tasks[Cancellable.task_no] = [task, group, None]
		self.task_no = Cancellable.task_no  # For s