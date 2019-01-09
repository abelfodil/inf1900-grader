# Olivier Dion - 2019

from urwid import (Columns,
                   Pile,
                   WidgetContainerMixin,
                   WidgetPlaceholder)

from collections import deque

class WidgetException(Exception):

    def __init__(self, msg, *kargs, **kwargs):
        super().__init__(msg, *kargs, **kwargs)

# inherit from WidgetContainerMixer instead??
class TreeWidget(WidgetPlaceholder):

    def __init__(self, widget, *args, **kwargs):
        super().__init__(widget, *args, **kwargs)

    def split_horizontally(self, widget):
        self.original_widget = TreeWidget(Columns([self.original_widget, widget])).original_widget

    def split_vertically(self, widget):
        self.original_widget = TreeWidget(Pile([self.original_widget, widget])).original_widget

    def remove_widget(self, node):

        queue = deque([self.original_widget])

        while len(queue) != 0:

            container = queue.pop()

            for widget, options in container.contents.items():

                if widget is node:
                    container.contents.remove((widget, options))
                    return widget, options

                if (isinstance(widget, WidgetContainerMixin) or
                    isinstance(widget, TreeWidget)):
                    queue.appendleft(widget)

from urwid import Text

from src.views.hydra import Hydra

class HydraWidget(Text):

    def __init__(self, hydra=None, *kargs, **kwargs):

        super().__init__("", *kargs, **kwargs)

        self.hydra = hydra

        if hydra is not None:
            self.parse_hydra()

        # Glitch
        self._selectable = True


    def set_hydra(self):
        self.hydra = hydra
        self.parse_hydra()

    def parse_hydra(self):

        markup = []
        kbd    = {}

        # To refractor if better idea on how to make that

        markup.append(("", f"{self.hydra.info}\n"))

        for letter, head in self.hydra.heads.items():

            kbd[letter] = head

            if head.exit_ == Hydra.t:
                tmp_letter = ("blue_head", head.letter)
            else:
                tmp_letter = ("red_head", head.letter)
            if head.hint != "":
                markup.append(("", "["))
                markup.append(tmp_letter)
                markup.append(("", f"]: {head.hint}"))
            else:
                markup.append(tmp_letter)

            markup.append(("", ", "))

        markup.pop()

        self.kbd = kbd
        self.set_text(markup if len(markup) != 0 else "")

    def keypress(self, size, key):

        if key in self.kbd:
            t = self.kbd[key]()
            return None

        return key

    def add_heads(self, heads):
        if self.hydra is not None:
            self.hydra.add_heads(heads)
            self.parse_hydra()


from urwid import Edit


class Dlist:

    def __init__(self, data=None):

        self.data = data
        self.next = self
        self.prev = self

    @staticmethod
    def __add(new, prev, next):
        next.prev = new
        new.next = next
        new.prev = prev
        prev.next = new

    def add(self, new):
        Dlist.__add(new, self, self.next)

    def add_tail(self, new):
        Dlist.__add(new, self.prev, self)

    def remove(self):

        self.prev.next_ = self.next
        self.next.prev_ = self.prev

        self.next = self
        self.prev = self

from urwid import connect_signal, emit_signal, disconnect_signal, register_signal

class Controller:

    def __init__(self):
        self.signals = {}

    def emit(self, signal, *args):
        emit_signal(self, signal, *args)

    def connect(self, signal, slot, user_args=None, weak_args=None):
        return connect_signal(self, signal, slot, weak_args=weak_args, user_args=user_args)

    def disconnect(self, signal, key):
        return disconect_signal(self, signal, key)

class MiniBuff(Edit, Controller):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.history = Dlist("")
        self.current = self.history

        self.kbd = {
            "enter":  self.flush,
            "ctrl p": self.previous_history,
            "ctrl n": self.next_history,
            "ctrl r": self.reverse_i_search
        }

    def keypress(self, size, key):

        if key in self.kbd:
            self.kbd[key]()

        super().keypress(size, key)

    def flush(self):

        txt = self.get_edit_text()

        if txt != self.current.prev.data:
            self.current.data = txt
            self.current.add(Dlist(""))
            self.current = self.current.next
        else:
            self.current.data = ""

        self.history = self.current

        self.set_edit_text("")

        self.emit("on_flush", self.get_last_text())

    def previous_history(self):
        self.history.data = self.get_edit_text()
        self.history = self.history.prev
        self.update_text(self.history.data)

    def next_history(self):
        self.history.data = self.get_edit_text()
        self.history = self.history.next
        self.update_text(self.history.data)

    def reverse_i_search(self):
        pass

    def update_text(self, text):
        self.set_edit_text(text)
        self.set_edit_pos(len(text))

    def get_last_text(self):
        return self.current.prev.data

register_signal(MiniBuff, ["on_flush"])

if __name__ == "__main__":

    from urwid import MainLoop, Filler, SolidFill, ExitMainLoop, BoxAdapter

    def quit():
        raise ExitMainLoop()

    mb = MiniBuff()

    key_1 = mb.connect("on_flush", quit, [(1,2)])

    l = MainLoop(Filler(mb))

    l.run()
