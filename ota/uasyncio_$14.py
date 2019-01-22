DEBUG and __debug__:
            log.debug("StreamReader.readline(): %s", buf)
        return buf

    def aclose(self):
        yield IOReadDone(self.polls)
        self.ios.close()

    def __repr__(self):
        return "<StreamReader %r %r>" % (self.polls, self.ios)


class StreamWriter:

    def __init__(self, s, extra):
        self.s = s
        self.extra = extra

    def awrite(self, buf, off=0, sz=-1):
        # This method is called awrite (async write) to not proliferate
        # incompatibility with original asyncio. Unlike original asyncio
        # whose .write() method is both not a coroutine and guaranteed
        # to return immediately (which means it has to buffer all the
        # data), this method is a coroutine.
        if sz == -1:
            sz = len(buf) - off
        if DEBUG and __debug__:
            log.debug("StreamWriter.awrite(): spooling %d bytes", sz)
        while True:
            res = self.s.write(buf, off, sz)
            # If we spooled every