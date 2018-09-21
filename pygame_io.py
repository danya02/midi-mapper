import pygame
import pygame.midi
import common


class PygameInput(common.Input):
    """Interface to Input of pygame.midi."""

    def __init__(self, id: int):
        pygame.init()
        pygame.midi.init()
        self.input = pygame.midi.Input(id)

    def poll(self):
        return self.input.poll()

    def get(self, count: int = 1, block: bool = False):
        buffer = []
        while len(buffer) != count:
            buffer += self.input.read(1)
            if not block and not self.poll():
                break
        messages = []
        for i in buffer:
            m = common.MIDIMessage()
            m.status = i[0][0]
            m.data = i[0][1:]
            messages += [m]
        return messages


class PygameOutput(common.Output):
    """Interface to Output of pygame.midi."""

    def __init__(self, id: int):
        pygame.init()
        pygame.midi.init()
        self.output = pygame.midi.Output(id, latency=0)

    def put(self, message: common.MIDIMessage, callback: callable = None):
        self.output.write([[message.status] + message.data, pygame.midi.time()])
        callback(message)

