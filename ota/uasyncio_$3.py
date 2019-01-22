       args = self.runq.popleft()
                    l -= 1
                    if __debug__ and DEBUG:
                        log.info("Next callback to run: %s", (cb, args))
                    cb(*args)
                    continue

                if __debug__ and DEBUG:
                    log.info("Next coroutine to run: %s", (cb, args))
                self.cur_task = cb
                delay = 0
                try:
                    if args is ():
                        ret = next(cb)
                    else:
                        ret = cb.send(*args)
                    if __debug__ and DEBUG:
                        log.info("Coroutine %s yield result: %s", cb, ret)
                    if isinstance(ret, SysCall1):
                        arg = ret.arg
                        if isinstance(ret, SleepMs):
                            delay = arg
                        elif isinstance(ret, IORead):
                            cb.pend_throw(False)
                      