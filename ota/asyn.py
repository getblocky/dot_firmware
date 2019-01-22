# asyn.py 'micro' synchronisation primitives for uasyncio
# Test/demo programs asyntest.py, barrier_test.py
# Provides Lock, Event, Barrier, Semaphore, BoundedSemaphore, Condition,
# NamedTask and Cancellable classes, also sleep coro.
# Uses low_priority where available and appropriate.
# Updated 31 Dec 2017 for uasyncio.core V1.6 and to provide task cancellation.

# The MIT License (MIT)
#
# Copyright (c) 2017 Peter Hinch
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Sof