#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from urwid import AttrMap, Columns, Filler, LineBox, Pile, ProgressBar

from src.views.base.button import Button
from src.views.base.controller import Controller
from src.views.base.signal import Signal
from src.views.base.tree import TreeWidget
from src.views.base.tui import TUI


@Signal("on_quit")
class AbstractPanel(Controller):

    def __init__(self, widget, form):

        super().__init__()

        confirm  = LineBox(AttrMap(Button("Confirm",
                                          on_press=self.confirm,
                                          align="center"),
                                   "default",
                                   "confirm_button"))

        abort    = LineBox(AttrMap(Button("Abort",
                                          on_press=self.abort,
                                          align="center"),
                                   "default",
                                   "abort_button"))

        self.buttons_column  = Columns([confirm, abort])

        bar      = ProgressBar("progress_low",
                               "progress_hight",
                               current=10)

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
        self.form = form
        self.root = Filler(self.tree, valign="top")

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
