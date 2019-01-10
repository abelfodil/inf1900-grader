#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from collections import deque

from urwid import Columns, Pile, WidgetContainerMixin, WidgetWrap, WidgetDecoration


# inherit from WidgetContainerMixer instead??
class TreeWidget(WidgetWrap):

    def __init__(self, widget, *args, **kwargs):
        super().__init__(widget, *args, **kwargs)

        self.keybind = {}
        self.aliases  = {}

    def split_horizontally(self, widget):
        if isinstance(self._w, Columns):
            self._w.contents.append((widget, self._w.options()))
        else:
            self._w = Columns([self._w, widget])

    def split_vertically(self, widget):
        if isinstance(self._w, Pile):
            self._w.contents.append((widget, self._w.options()))
        else:
            self._w = Pile([self._w, widget])

    def bind(self, key, callback):
        self.keybind[key] = callback

    def set_aliases(self, aliases):

        if not isinstance(aliases, list):
            aliases = [aliases]

        for alias, target in aliases:
            self.aliases[alias] = target

    def remove_widget(self, node):

        queue = deque([self._w])

        while len(queue) != 0:

            container = queue.pop()

            for widget, options in container.contents.items():

                if widget is node:
                    container.contents.remove((widget, options))
                    return widget, options

                if (isinstance(widget, WidgetContainerMixin) or
                    isinstance(widget, TreeWidget)):
                    queue.appendleft(widget)

    def keypress(self, size, key):

        if key in self.aliases:
            key = self.aliases[key]

        if key in self.keybind:
            self.keybind[key](size, key)
            return None

        return key

    def focus_next_node(self, *kargs, **kwargs):
        self.focus_node(1)

    def focus_prev_node(self, *kargs, **kwargs):
        self.focus_node(-1)

    # Best way I found to fetch surrounding node
    def focus_node(self, direction):

        focus_path = self._w.get_focus_path()

        while len(focus_path):

            focus_path.append(focus_path.pop() + direction)

            try:
                self._w.set_focus_path(focus_path)
                return
            except IndexError:
                focus_path.pop()

    # for debugging
    def print_node(self, node, out):

        queue = [(node, 0)]

        f = open(out, "w")

        while len(queue):

            (w, lvl) = queue.pop()

            if isinstance(w, TreeWidget):
                queue.append((w._w, lvl + 1))
            elif isinstance(w, WidgetContainerMixin):
                for c in w.contents:
                    queue.append((c[0], lvl + 1))
            elif isinstance(w, WidgetDecoration):
                queue.append((w.original_widget, lvl + 1))

            indent = " " * lvl

            f.write(f"{indent}{type(w)}\n")

        f.close()
