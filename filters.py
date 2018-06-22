#!/usr/bin/python3
import common
import time


class DelayFilter(common.Filter):
    """Delays messages by a certain length of time. Exact time not guaranteed."""

    def __init__(self, input, output, delay=0.1):
        self.name = 'Delay filter for {} s'.format(delay)
        self.delay = delay
        self.stack = []
        super().__init__(input, output)

    def run(self):
        while self.running:
            if self.input.poll():
                self.stack.append([self.input.get(1)[0], time.time() + self.delay])
            for i in self.stack:
                if time.time() >= i[1]:
                    self.output.put(i[0])
