#!/usr/bin/python3
import common
import time


class DelayFilter(common.Filter):
    """Delays messages by a certain length of time. Exact time not guaranteed."""

    def __init__(self, output, delay=0.1):
        self.name = 'Delay filter for {} s'.format(delay)
        self.delay = delay
        self.stack = []
        super().__init__(output)

    def run(self):
        while self.running:
            if len(self.buffer):
                m = self.buffer.pop()
                self.stack.append([m, time.time() + self.delay])
            for i in self.stack:
                if time.time() >= i[1]:
                    self.output.put(i[0][0])
                    i[0][1](i[0][0])
