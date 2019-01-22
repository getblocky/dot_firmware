cheduling
        if __debug__ and DEBUG:
            log.debug("Sleeping for: %s", delay)
        time.sleep_ms(delay)

    def run_forever(self):
        cur_task = [0, 0, 0]
        while True:
            # Expire entries in waitq and move them to runq
            tnow = self.time()
            while self.waitq:
                t = self.waitq.peektime()
                delay = time.ticks_diff(t, tnow)
                if delay > 0:
                    break
                self.waitq.pop(cur_task)
                if __debug__ and DEBUG:
                    log.debug("Moving from waitq to runq: %s", cur_task[1])
                self.call_soon(cur_task[1], *cur_task[2])

            # Process runq
            l = len(self.runq)
            if __debug__ and DEBUG:
                log.debug("Entries in runq: %d", l)
            while l:
                cb = self.runq.popleft()
                l -= 1
                args = ()
                if not isinstance(cb, type_gen):
             