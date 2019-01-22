ter_ms(0, coro)
        # CPython asyncio incompatibility: we don't return Task object

    def call_soon(self, callback, *args):
        if __debug__ and DEBUG:
            log.debug("Scheduling in runq: %s", (callback, args))
        self.runq.append(callback)
        if not isinstance(callback, type_gen):
            self.runq.append(args)

    def call_later(self, delay, callback, *args):
        self.call_at_(time.ticks_add(self.time(), int(delay * 1000)), callback, args)

    def call_later_ms(self, delay, callback, *args):
        if not delay:
            return self.call_soon(callback, *args)
        self.call_at_(time.ticks_add(self.time(), delay), callback, args)

    def call_at_(self, time, callback, args=()):
        if __debug__ and DEBUG:
            log.debug("Scheduling in waitq: %s", (time, callback, args))
        self.waitq.push(time, callback, args)

    def wait(self, delay):
        # Default wait implementation, to be overriden in subclasses
        # with IO s