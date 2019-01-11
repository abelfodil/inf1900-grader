#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from urwid import Filler, Pile

from src.views.base.controller import Controller
from src.views.base.signal import Signal
from src.views.base.tree import TreeWidget
from src.views.base.tui import TUI


@Signal("on_quit")
class AbstractPanel(Controller):

    def __init__(self, widget, form):

        super().__init__()

        tree = TreeWidget(widget)

        tree.bind("up", tree.focus_prev_node)
        tree.bind("down", tree.focus_next_node)

        tree.set_aliases(
            [
                ("ctrl p", "up"),
                ("shift tab", "up"),
                ("ctrl n", "down"),
                ("tab", "down"),
                ("ctrl f", "right"),
                ("ctrl b", "left"),
            ]
        )

        self.tree = tree
        self.root = Pile([Filler(self.tree, valign="top")])
        self.form = form

    def confirm(self, button):
        try:
            TUI.clear()
            self.form.submit()
            self.emit("on_quit", button)
        except Exception as e:
            TUI.print(str(e))

    def abort(self, button):
        TUI.clear()
        self.emit("on_quit", button)
