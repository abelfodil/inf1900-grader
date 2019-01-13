from enum import IntEnum, auto
from itertools import chain

from urwid import Columns, Pile as Rows, WidgetWrap


class GridPolicy(IntEnum):
    HORIZONTAL = auto()
    VERTICAL = auto()


class Grid(WidgetWrap):
    def __init__(self, rows, policy=GridPolicy.HORIZONTAL):
        super().__init__(Rows([Columns(row) for row in rows]))
        self.contents = list(chain.from_iterable(rows))

        self.n = len(rows)
        self.m = round(len(self.contents) / self.n)

        self.i = 0
        self.j = 0

        self.focus(self.i, self.j)

        self.keybinds = {
            "up"       : lambda: self.focus_vertical(-1),
            "down"     : lambda: self.focus_vertical(1),
            "tab"      : self.focus_next,
            "shift tab": self.focus_prev
        }

        self.aliases = {
            "ctrl f": "left",
            "ctrl b": "right",
            "ctrl p": "up",
            "ctrl n": "down"
        }

        self.policy = policy

    def focus_horizontal(self, direction):

        j = self.j
        i = self.i

        while True:
            j += direction
            i += j // self.m
            j %= self.m
            i %= self.n

            try:
                self.focus(i, j)
                break
            except IndexError:
                pass

    def focus_vertical(self, direction):

        i = self.i
        j = self.j

        while True:
            i += direction
            j += i // self.n
            i %= self.n
            j %= self.m

            try:
                self.focus(i, j)
                break
            except IndexError:
                pass

    def focus_next(self):
        if self.policy == GridPolicy.HORIZONTAL:
            return self.focus_horizontal(1)

        return self.focus_vertical(1)

    def focus_prev(self):
        if self.policy == GridPolicy.HORIZONTAL:
            return self.focus_horizontal(-1)

        return self.focus_vertical(-1)

    def focus_first(self):
        # TODO: fix buggy behaviour
        self._w.set_focus_path([0, 0])

    def focus(self, i, j):
        self._w.set_focus_path([i, j])
        self.i = i
        self.j = j

    def keypress(self, size, key):

        if key in self.aliases:
            key = self.aliases[key]

        if key in self.keybinds:
            self.keybinds[key]()
            return None

        return super().keypress(size, key)
