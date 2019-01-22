

            # Wait until next waitq task or I/O availability
            delay = 0
            if not self.runq:
                delay = -1
                if self.waitq:
                    tnow = self.time()
                    t = self.waitq.peektime()
                    delay = time.ticks_diff(t, tnow)
                    if delay < 0:
                        delay = 0
            self.wait(delay)

    def run_until_complete(self, coro):
        def _run_and_stop():
            yield from coro
            yield StopLoop(0)
        self.call_soon(_run_and_stop())
        self.run_forever()

    def stop(self):
        self.call_soon((lambda: (yield StopLoop(0)))())

    def close(self):
        pass


class SysCall:

    def __init__(self, *args):
        self.args = args

    def handle(self):
        raise NotImplementedError

# Optimized syscall with 1 arg
class SysCall1(SysCall):

    def __init__(self, arg):
        self.arg = arg

class StopLoop(SysCall1):
    pass

class I