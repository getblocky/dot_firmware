cio.sleep_ms(rem)

# Anonymous cancellable tasks. These are members of a group which is identified
# by a user supplied name/number (default 0). Class method cancel_all() cancels
# all tasks in a group and awaits confirmation. Confirmation of ending (whether
# normally or by cancellation) is signalled by a task calling the _stopped()
# class method. Handled by the @cancellable decorator.


class Cancellable():
	
	task_no = 0  # Generated task ID, index of tasks dict
	tasks = {}  # Value is [coro, group, barrier] indexed by integer task_no

	@classmethod
	def _cancel(cls, task_no):
		task = cls.tasks[task_no][0]
		core.asyncio.cancel(task)

	@classmethod
	async def cancel_all(cls, group=0, nowait=False):
		tokill = cls._get_task_nos(group)
		barrier = Barrier(len(tokill) + 1)  # Include this task
		for task_no in tokill:
			cls.tasks[task_no][2] = barrier
			cls._cancel(task_no)
		if nowait:
			barrier.trigger()
		else:
			await barrier

	@classmethod
	def _is_running(cls, group=0):
		t