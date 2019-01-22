er(self, sock, cb, *args):
        if DEBUG and __debug__:
            log.debug("add_reader%s", (sock, cb, args))
        if args:
            self.poller.register(sock, select.POLLIN)
            self.objmap[id(sock)] = (cb, args)
        else:
            self.poller.register(sock, select.POLLIN)
            self.objmap[id(sock)] = cb

    def remove_reader(self, sock):
        if DEBUG and __debug__:
            log.debug("remove_reader(%s)", sock)
        self.poller.unregister(sock)
        del self.objmap[id(sock)]

    def add_writer(self, sock, cb, *args):
        if DEBUG and __debug__:
            log.debug("add_writer%s", (sock, cb, args))
        if args:
            self.poller.register(sock, select.POLLOUT)
            self.objmap[id(sock)] = (cb, args)
        else:
            self.poller.register(sock, select.POLLOUT)
            self.objmap[id(sock)] = cb

    def remove_writer(self, sock):
        if DEBUG and __debug__:
            log.debug("remove_writer(%s)", so