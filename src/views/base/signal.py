from enum import Enum

from urwid import register_signal


class SignalType(Enum):
    QUIT = "on_quit"
    SWAP = "on_swap"
    PRESS = "on_press"
    FLUSH = "on_flush"


class Signal:

    def __init__(self, *args):
        self.signals = args

    def __call__(self, *args):
        cls = args[0]
        register_signal(cls, self.signals)
        return cls
