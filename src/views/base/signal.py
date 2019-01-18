from enum import Enum


class SignalType(Enum):
    QUIT = "on_quit"
    SWAP = "on_swap"
    CLICK = "on_click"
    FLUSH = "on_flush"
