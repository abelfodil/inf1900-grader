from urwid import Text, connect_signal, emit_signal

from src.views.base.signal import Signal


@Signal("on_press")
class Button(Text):

    def __init__(self, markup, on_press=None, *kargs, **kwargs):

        super().__init__(f"[{markup}]", *kargs, **kwargs)

        # Glitch
        self._selectable = True

        if callable(on_press):
            connect_signal(self, "on_press", on_press)

    def keypress(self, size, key):
        if key == "enter":
            emit_signal(self, "on_press", self)
            return None

        return key
