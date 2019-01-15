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
            "up"       : lambda: self.focus_prev_vertical(),
            "down"     : lambda: self.focus_next_vertical(),
            "tab"      : self.focus_next,
            "shift tab": self.focus_prev
        }

        self.aliases = {
            "ctrl f": "left",
            "ctrl b": "right",
            "ctrl p": "up",
            "ctrl n": "down"
        }

        self.parent = None

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

        j = self.j
        i = self.i

        while True:
            i += direction
            j += i // self.n
            j %= self.m
            i %= self.n

            try:
                self.focus(i, j)
                break
            except IndexError:
                pass

    def focus_next(self):

        while True:
            child = self.current_focus()
            end_of_grid = self.__is_last()

            if isinstance(child, Grid):
                child.focus_next()
            elif end_of_grid:
                if self.parent is not None and not self.parent.__is_last():
                    return self.parent.focus_horizontal(1)
            else:
                self.focus_horizontal(1)

            if self.current_focus().selectable():
                break

    def focus_next_vertical(self):

        while True:
            child = self.current_focus()
            end_of_grid = self.__is_last()

            if isinstance(child, Grid):
                child.focus_next()
            elif end_of_grid:
                if self.parent is not None and not self.parent.__is_last():
                    return self.parent.focus_vertical(1)
            else:
                self.focus_vertical(1)

            if self.current_focus().selectable():
                break

    def focus_prev(self):

        while True:
            focus = self.current_focus()
            beg_of_grid = self.__is_first()

            if isinstance(focus, Grid):
                focus.focus_prev()
            elif beg_of_grid:
                if self.parent is not None and not self.parent.__is_first():
                    return self.parent.focus_horizontal(-1)
            else:
                self.focus_horizontal(-1)

            if self.current_focus().selectable():
                break

    def focus_prev_vertical(self):

        while True:
            focus = self.current_focus()
            beg_of_grid = self.__is_first()

            if isinstance(focus, Grid):
                focus.focus_prev()
            elif beg_of_grid:
                if self.parent is not None and not self.parent.__is_first():
                    return self.parent.focus_vertical(-1)
            else:
                self.focus_vertical(-1)

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
