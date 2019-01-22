le
                        pass
                    elif ret is False:
                        # Don't reschedule
                        continue
                    else:
                        assert False, "Unsupported coroutine yield value: %r (of type %r)" % (ret, type(ret))
                except StopIteration as e:
                    if __debug__ and DEBUG:
                        log.debug("Coroutine finished: %s", cb)
                    continue
                except CancelledError as e:
                    if __debug__ and DEBUG:
                        log.debug("Coroutine cancelled: %s", cb)
                    continue
                # Currently all syscalls don't return anything, so we don't
                # need to feed anything to the next invocation of coroutine.
                # If that changes, need to pass that value below.
                if delay:
                    self.call_later_ms(delay, cb)
                else:
                    self.call_soon(cb)