# Olivier Dion - 2019

from urwid import Columns, Pile, WidgetPlaceholder, WidgetContainerMixin

from collections import deque

class WidgetException(Exception):

    def __init__(msg, *kargs, **kwargs):
        super().__init__(msg, *kargs, **kwargs)

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

            for (widget, options) in container.contents:

                if widget is node:
                    container.contents.remove((widget, options))
                    return

                if (isinstance(widget, WidgetContainerMixin) or
                    isinstance(widget, TreeWidget)):
                    queue.appendleft(widget)





from urwid import Text

from hydra import Hydra

class HydraWidget(Text):

    def __init__(self, hydra, *kargs, **kwargs):

        self.hydra = hydra

        (text, kbd) = self.parse_hydra()

        self.kbd = kbd

        super().__init__(text, *kargs, **kwargs)

        self._selectable = True


    def parse_hydra(self):

        markup = []
        kbd    = {}

        markup.append(("", f"{self.hydra.info}\n"))

        for letter, head in self.hydra.heads.items():

            kbd[letter] = head

            tmp_letter = None

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

        return (markup, kbd)

    def keypress(self, size, key):

        if key in self.kbd:
            t = self.kbd[key]()
            return None

        return key


from urwid import Edit


class Dlist:

    def __init__(self, data=None):

        self.data = data
        self._next = self
        self.prev = self

    @staticmethod
    def __add(new, prev, _next):
        _next.prev = new
        new._next = _next
        new.prev = prev
        prev._next = new

    def add(self, new):
        Dlist.__add(new, self, self._next)

    def add_tail(self, new):
        Dlist.__add(new, self.prev, self)

    def remove(self):

        self.prev.next_ = self._next
        self._next.prev_ = self.prev

        self._next = self
        self.prev = self

class MiniBuff(Edit):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.history = Dlist("")

        self.kbd = {
            "enter": self.flush,
            "ctrl p": self.previous_history,
            "ctrl n": self.next_history,
            "ctrl r": self.reverse_i_search
        }

    def keypress(self, size, key):

        if key in self.kbd:
            self.kbd[key]()
        else:
            print(key)

        super().keypress(size, key)

    def flush(self):

        txt = self.get_edit_text()

        if txt != self.history.prev.data:
            self.history.data = txt
            self.history.add(Dlist(""))
            self.history = self.history._next

        self.set_edit_text("")

    def previous_history(self):

        if self.history.prev != None:
            self.history.data = self.get_edit_text()
            self.history = self.history.prev
            self.update_text(self.history.data)

    def next_history(self):

        if self.history._next != None:
            self.history.data = self.get_edit_text()
            self.history = self.history._next
            self.update_text(self.history.data)

    def reverse_i_search(self):
        pass

    def update_text(self, text):
        self.set_edit_text(text)
        self.set_edit_pos(len(text))

if __name__ == "__main__":

    from urwid import MainLoop, Filler

    m = MiniBuff()

    f = Filler(m)

    l = MainLoop(f)

    l.run()
