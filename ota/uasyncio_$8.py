k__ = None
        raise _stop_iter

_stop_iter = StopIteration()
sleep_ms = SleepMs()


def cancel(coro):
    prev = coro.pend_throw(CancelledError())
    if prev is False:
        _event_loop.call_soon(coro)


class TimeoutObj:
    def __init__(self, coro):
        self.coro = coro


def wait_for_ms(coro, timeout):

    def waiter(coro, timeout_obj):
        res = yield from coro
        if __debug__ and DEBUG:
            log.debug("waiter: cancelling %s", timeout_obj)
        timeout_obj.coro = None
        return res

    def timeout_func(timeout_obj):
        if timeout_obj.coro:
            if __debug__ and DEBUG:
                log.debug("timeout_func: cancelling %s", timeout_obj.coro)
            prev = timeout_obj.coro.pend_throw(TimeoutError())
            #print("prev pend", prev)
            if prev is False:
                _event_loop.call_soon(timeout_obj.coro)

    timeout_obj = TimeoutObj(_event_loop.cur_task)
    _event_loop.call_later_ms(timeout, timeout_func, time