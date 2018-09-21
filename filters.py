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

class TransposeFilter(common.Filter):
    """Transposes note messages."""

    def __init__(self,output,transpose=1):
        self.name = f'Transpose filter ({transpose} semitones)'
        self.transpose = transpose
        super().__init__(output)
    
    def run(self):
        while self.running:
            while len(self.buffer):
                m = self.buffer.pop()
                if m.status>>4 in [0b1000,0b1001]:
                    m.data1 += self.transpose
                    if m.data1<0:
                        print(f'Transpose bottomed out! Clipping {m.data} to 0!')
                        m.data=0
                    if m.data1>0b01111111:
                        print(f'Transpose topped out! Clipping {m.data} to {0b01111111}!')
                        m.data = 0b01111111
                self.output.put(m)

