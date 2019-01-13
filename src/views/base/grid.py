from urwid import Columns
from urwid import Pile as Rows
from urwid import WidgetWrap

from itertools import chain

class GridException(Exception):
    pass

class Grid(WidgetWrap):

    policies = ("horizontal", "vertical")

    def __init__(self, rows):

        self._w = Rows([Columns(row) for row in rows])
        self.contents = list(chain.from_iterable(rows))

        self.n = len(rows)
        self.m = round(len(self.contents) / self.n)


        self.i = 0
        self.j = 0

        self.focus(self.i, self.j)

        self.aliases = {}
        self.kbd     = {}

        self.policy = "horizontal"

    def set_policy(self, policy):

        if policy not in Grid.policies:
            raise GridException("Bad policy: {policy}")

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

        if self.policy == "horizontal":
            return self.focus_horizontal(1)

        return self.focus_vertical(1)

    def focus_prev(self):

        if self.policy == "horizontal":
            return self.focus_horizontal(-1)

        return self.focus_vertical(-1)

    def focus(self, i, j):
        self._w.set_focus_path([i, j])
        self.i = i
        self.j = j


    def alises(self, aliases):

        if not isinstance(aliases, list):
            aliases = list(aliases)

        for alias in aliases:
            self.aliases[alias[0]] = alias[1]

    def bind(self, kbds):

        if not isinstance(kbds, list):
            kbds = list(kbds)

        for kbd in kbds:
            self.kbd[kbd[0]] = kbd[1]

    def keypress(self, size, key):

        if key in self.aliases:
            key = self.aliases[key]

        if key in self.kbd:
            self.kbd[key]()
            return None

        return key
