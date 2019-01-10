#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from urwid import Text

from src.views.base.controller import Controller
from src.views.base.signal import Signal


@Signal("on_press")
class Button(Text, Controller):

    def __init__(self, markup, on_press=None, *kargs, **kwargs):

        super().__init__(f"[{markup}]", *kargs, **kwargs)

        # Glitch
        self._selectable = True

        if callable(on_press):
            self.connect("on_press", on_press)

    def keypress(self, size, key):

        if key == "enter":
            self.emit("on_press", self)
            return None

        return key
