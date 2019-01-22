by enabling tasks which have been
# cancelled to leave the task queue as soon as possible.

# Uses low_priority if available

class Barrier():
	
	def __init__(self, participants, func=None, args=()):
		self._participants = participants
		self._func = func
		self._args = args
		self._reset(True)

	def __await__(self):
		self._update()
		if self._at_limit():  # All other threads are also at limit
			if self._func is not None:
				launch(self._func, self._args)
			self._reset(not self._down)  # Toggle direction to release others
			return

		direction = self._down
		while True:  # Wait until last waiting thread changes the direction
			if direction != self._down:
				return
			yield

	__iter__ = __await__

	def trigger(self):
		self._update()
		if self._at_limit():  # All other threads are also at limit
			if self._func is not None:
				launch(self._func, self._args)
			self._reset(not self._down)  # Toggle direction to release others

	def _reset(self, down):
		self._down = down
		self._