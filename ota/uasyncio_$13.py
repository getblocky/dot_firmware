is should not happen for real sockets, but can easily
            # happen for stream wrappers (ssl, websockets, etc.)
            #log.warn("Empty read")
        if not res:
            yield IOReadDone(self.polls)
        return res

    def readexactly(self, n):
        buf = b""
        while n:
            yield IORead(self.polls)
            res = self.ios.read(n)
            assert res is not None
            if not res:
                yield IOReadDone(self.polls)
                break
            buf += res
            n -= len(res)
        return buf

    def readline(self):
        if DEBUG and __debug__:
            log.debug("StreamReader.readline()")
        buf = b""
        while True:
            yield IORead(self.polls)
            res = self.ios.readline()
            assert res is not None
            if not res:
                yield IOReadDone(self.polls)
                break
            buf += res
            if buf[-1] == 0x0a:
                break
        if 