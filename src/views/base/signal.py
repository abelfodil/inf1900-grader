from enum import Enum


class SignalType(Enum):
    QUIT = "on_quit"
    SWAP = "on_swap"
    PRESS = "on_press"
    FLUSH = "on_flush"
