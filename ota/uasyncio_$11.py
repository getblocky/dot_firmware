ck)
        try:
            self.poller.unregister(sock)
            self.objmap.pop(id(sock), None)
        except OSError as e:
            # StreamWriter.awrite() first tries to write to a socket,
            # and if that succeeds, yield IOWrite may never be called
            # for that socket, and it will never be added to poller. So,
            # ignore such error.
            if e.args[0] != uerrno.ENOENT:
                raise

    def wait(self, delay):
        if DEBUG and __debug__:
            log.debug("poll.wait(%d)", delay)
        # We need one-shot behavior (second arg of 1 to .poll())
        res = self.poller.ipoll(delay, 1)
        #log.debug("poll result: %s", res)
        # Remove "if res" workaround after
        # https://github.com/micropython/micropython/issues/2716 fixed.
        if res:
            for sock, ev in res:
                cb = self.objmap[id(sock)]
                if ev & (select.POLLHUP | select.POLLERR):
                    # These events a