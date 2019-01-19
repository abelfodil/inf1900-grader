from collections import Callable

from urwid import AttrMap, LineBox, Text, WidgetWrap, connect_signal, emit_signal

CLICK_SIGNAL = "on_click"


class Button(WidgetWrap):
    signals = [CLICK_SIGNAL]

    def __init__(self, text: str, palette: str, callback: Callable):
        connect_signal(self, CLICK_SIGNAL, callback)

        widget = LineBox(AttrMap(Text(f"[{text}]", align="center"), "default", palette))
        super().__init__(widget)

        # Glitch
        self._w.base_widget._selectable = True

    def keypress(self, size, key):
        if key == "enter":
            emit_signal(self, CLICK_SIGNAL)
            return None

        return key
