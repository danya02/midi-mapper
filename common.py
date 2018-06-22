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


class Input:
    """Superclass for all MIDI message sources."""

    def poll(self) -> bool:
        """Is there new data on wire?"""
        return False

    def get(self, count: int = 1, block: bool = False) -> [MIDIMessage]:
        """Return this many MIDI messages. If block, wait until this many are in the buffer before returning."""
        if block:
            while 1:
                pass
        return []


class Output:
    """Superclass for all MIDI message sinks."""

    def put(self, message: MIDIMessage, callback: callable = None):
        """Send this MIDI message on wire. When done sending. run the callback with the message as parameter."""
        if callback is not None:
            callback(message)
        return


class Filter(threading.Thread):
    """Superclass for all MIDI filters."""

    def __init__(self, input: Input, output: Output):
        if not 'name' in self.__dict__:
            self.name = 'Passthru MIDI filter'
        super().__init__(name=self.name)
        self.input = input
        self.output = output
        self.running = True
        self.start()

    def run(self):
        while self.running:
            if self.input.poll():
                self.output.put(self.input.get(1)[0])
