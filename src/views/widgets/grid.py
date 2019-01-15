from enum import auto

from urwid import Columns, Pile as Rows, WidgetWrap


class GridPolicy:
    HORIZONTAL = auto()
    VERTICAL = auto()


class Grid(WidgetWrap):
    def __init__(self, rows):

        m = 1
        cols = []

        for row in rows:
            if len(row) > m:
                m = len(row)

            for c in row:
                if isinstance(c, Grid):
                    c.parent = self

            cols.append(Columns(row))

        super().__init__(Rows(cols))

        self.n = len(rows)
        self.m = m

        self.i = 0
        self.j = 0

        self.focus(self.i, self.j)

        self.keybinds = {
            "down" : lambda: self.focus_recursive(forward=True, horizontal=False),
            "up"   : lambda: self.focus_recursive(forward=False, horizontal=False),
            "right": lambda: self.focus_recursive(forward=True, horizontal=True),
            "left" : lambda: self.focus_recursive(forward=False, horizontal=True)
        }

        self.aliases = {
            "shift tab": "left",
            "tab"      : "right",
            "ctrl f"   : "left",
            "ctrl b"   : "right",
            "ctrl p"   : "up",
            "ctrl n"   : "down"
        }

        self.parent = None

    def focus_direction(self, forward: bool, horizontal: bool):

        j = self.j
        i = self.i
        direction = 1 if forward else -1

        while True:
            if horizontal:
                j += direction
                i += j // self.m
            else:
                i += direction
                j += i // self.n

            j %= self.m
            i %= self.n

            try:
                self.focus(i, j)
                break
            except IndexError:
                pass

    def focus_recursive(self, forward: bool, horizontal: bool):
        while True:
            child = self.current_focus()

            if isinstance(child, Grid):
                child.focus_recursive(forward, horizontal)
            elif not forward and self.__is_first():
                if self.parent is not None and not self.parent.__is_first():
                    return self.parent.focus_direction(forward, horizontal)
            elif forward and self.__is_last():
                if self.parent is not None and not self.parent.__is_last():
                    return self.parent.focus_direction(forward, horizontal)
            else:
                self.focus_direction(forward, horizontal)

            if self.current_focus().selectable():
                break

    def focus_first(self):
        self.focus(0, 0)

    def focus(self, i, j):
        self._w.base_widget.set_focus_path([i, j])
        self.i = i
        self.j = j

    def current_focus(self):
        return self._w.base_widget.contents[self.i][0].contents[self.j][0].base_widget

    def __is_last(self):
        return self.i == self.n - 1 and self.j == self.m - 1

    def __is_first(self):
        return self.i == 0 and self.j == 0

    def keypress(self, size, key):

        if key in self.aliases:
            key = self.aliases[key]

        if key in self.keybinds:
            self.keybinds[key]()
            return None

        return super().keypress(size, key)
