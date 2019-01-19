from enum import Enum


class SignalType(Enum):
    QUIT = "on_quit"
    CLICK = "on_click"
    FLUSH = "on_flush"
