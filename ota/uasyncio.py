# (c) 2014-2018 Paul Sokolovsky. MIT license.
import uerrno
import uselect as select
import usocket as _socket
import utime as time
import utimeq
import ucollections
type_gen = type((lambda: (yield))())

DEBUG = 0
log = None

def set_debug(val):
    global DEBUG, log
    DEBUG = val
    if val:
        import logging
        log = logging.getLogger("uasyncio.core")


class CancelledError(Exception):
    pass


class TimeoutError(CancelledError):
    pass


class EventLoop:

    def __init__(self, runq_len=100, waitq_len=100):
        self.runq = ucollections.deque((), runq_len, True)
        self.waitq = utimeq.utimeq(waitq_len)
        # Current task being run. Task is a top-level coroutine scheduled
        # in the event loop (sub-coroutines executed transparently by
        # yield from/await, event loop "doesn't see" them).
        self.cur_task = None

    def time(self):
        return time.ticks_ms()

    def create_task(self, coro):
        # CPython 3.4.2
        self.call_la