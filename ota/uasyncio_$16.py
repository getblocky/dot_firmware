_(self):
        return "<StreamWriter %r>" % self.s


def open_connection(host, port, ssl=False):
    if DEBUG and __debug__:
        log.debug("open_connection(%s, %s)", host, port)
    ai = _socket.getaddrinfo(host, port, 0, _socket.SOCK_STREAM)
    ai = ai[0]
    s = _socket.socket(ai[0], ai[1], ai[2])
    s.setblocking(False)
    try:
        s.connect(ai[-1])
    except OSError as e:
        if e.args[0] != uerrno.EINPROGRESS:
            raise
    if DEBUG and __debug__:
        log.debug("open_connection: After connect")
    yield IOWrite(s)
#    if __debug__:
#        assert s2.fileno() == s.fileno()
    if DEBUG and __debug__:
        log.debug("open_connection: After iowait: %s", s)
    if ssl:
        print("Warning: uasyncio SSL support is alpha")
        import ussl
        s.setblocking(True)
        s2 = ussl.wrap_socket(s)
        s.setblocking(False)
        return StreamReader(s, s2), StreamWriter(s2, {})
    return StreamReader(s), StreamWriter(s, {})


def start_se