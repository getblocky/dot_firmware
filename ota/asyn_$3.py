ued
class Event():
	
	def __init__(self, lp=False):  # Redundant arg retained for compatibility
		self.clear()

	def clear(self):
		self._flag = False
		self._data = None

	def __await__(self):
		while not self._flag:
			yield

	__iter__ = __await__

	def is_set(self):
		return self._flag

	def set(self, data=None):
		self._flag = True
		self._data = data

	def value(self):
		return self._data

# A Barrier synchronises N coros. Each issues await barrier.
# Execution pauses until all other participant coros are waiting on it.
# At that point the callback is executed. Then the barrier is 'opened' and
# execution of all participants resumes.

# The nowait arg is to support task cancellation. It enables usage where one or
# more coros can register that they have reached the barrier without waiting
# for it. Any coros waiting normally on the barrier will pause until all
# non-waiting coros have passed the barrier and all waiting ones have reached
# it. The use of nowait promotes efficiency 