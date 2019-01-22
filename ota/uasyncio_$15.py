thing, return immediately
            if res == sz:
                if DEBUG and __debug__:
                    log.debug("StreamWriter.awrite(): completed spooling %d bytes", res)
                return
            if res is None:
                res = 0
            if DEBUG and __debug__:
                log.debug("StreamWriter.awrite(): spooled partial %d bytes", res)
            assert res < sz
            off += res
            sz -= res
            yield IOWrite(self.s)
            #assert s2.fileno() == self.s.fileno()
            if DEBUG and __debug__:
                log.debug("StreamWriter.awrite(): can write more")

    # Write piecewise content from iterable (usually, a generator)
    def awriteiter(self, iterable):
        for buf in iterable:
            yield from self.awrite(buf)

    def aclose(self):
        yield IOWriteDone(self.s)
        self.s.close()

    def get_extra_info(self, name, default=None):
        return self.extra.get(name, default)

    def __repr_