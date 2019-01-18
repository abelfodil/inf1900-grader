from collections import Callable

from urwid import AttrMap, LineBox, MetaSignals, Text, WidgetWrap, connect_signal, emit_signal

from src.views.base.signal import SignalType


class Button(WidgetWrap, metaclass=MetaSignals):
    signals = [SignalType.CLICK]

    def __init__(self, text: str, palette: str, callback: Callable):
        connect_signal(self, SignalType.CLICK, callback)

        widget = LineBox(AttrMap(Text(f"[{text}]", align="center"), "default", palette))
        super().__init__(widget)

        # Glitch
        self._w.base_widget._selectable = True

    def keypress(self, size, key):
        if key == "enter":
            emit_signal(self, SignalType.CLICK)
            return None

        return key
