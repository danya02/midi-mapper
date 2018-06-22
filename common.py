#!/usr/bin/python3
import threading


class MIDIMessage:
    """Describes a single status+data group on wire."""

    def __setattr__(self, key, value):
        if key == 'status':
            if value not in range(128, 256):
                raise ValueError('Status must be a byte with MSB set to 1.')

        super().__setattr__(key, value)

    def __init__(self):
        self.status: int = 0
        self.data: [int] = []

    def is_system_message(self) -> bool:
        """Is this a system message?"""
        return self.status in range(int('f0', 16), int('ff', 16) + 1)

    def is_track_message(self) -> bool:
        """Is this a tracked message?"""
        return self.status in range(int('80', 16), int('ef', 16) + 1)

    def get_track(self) -> int:
        """Safe getter for this message's track."""
        if not self.is_track_message():
            raise ValueError('I am not a tracked message.')
        return (self.status & int('1111', 2)) + 1

    def get_data1(self) -> int:
        """Safe getter for DATA1 field."""
        try:
            return self.data[0]
        except IndexError:
            return 0

    def get_data2(self) -> int:
        """Safe getter for DATA2 field."""
        try:
            return self.data[1]
        except IndexError:
            return 0


class Input(threading.Thread):
    """Superclass for all MIDI message sources."""

    def __init__(self, output: Output):
        super().__init__()
        self.output = output
        self.start()

    def poll(self) -> bool:
        """Is there new data on wire?"""
        return False

    def get(self, count: int = 1, block: bool = False) -> [MIDIMessage]:
        """Return this many MIDI messages. If block, wait until this many are in the buffer before returning."""
        if block:
            while 1:
                pass
        return []

    def run(self):
        while 1:
            if self.poll():
                self.output.put(self.get(1)[0])


class Output:
    """Superclass for all MIDI message sinks."""

    def put(self, message: MIDIMessage, callback: callable = None):
        """Send this MIDI message on wire. When done sending. run the callback with the message as parameter."""
        if callback is not None:
            callback(message)
        return


class Filter(Output, threading.Thread):
    """Superclass for all MIDI filters."""

    def __init__(self, output: Output):
        if not 'name' in self.__dict__:
            self.name = 'Passthru MIDI filter'
        super().__init__(name=self.name)
        self.output = output
        self.running = True
        self.buffer = []
        self.start()

    def run(self):
        while self.running:
            if len(self.buffer):
                m = self.buffer.pop()
                self.output.put(m[0])
                m[1](m[0])

    def put(self, message: MIDIMessage, callback: callable = None):
        self.buffer.append([message, callback])
