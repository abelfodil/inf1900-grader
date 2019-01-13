from urwid import AttrMap, Filler, LineBox

from src.views.base.button import Button
from src.views.base.controller import Controller
from src.views.base.grid import Grid
from src.views.base.signal import Signal
from src.views.base.tui import TUI


@Signal("on_quit")
class AbstractPanel(Controller):

    def __init__(self, grid_elements, form):

        super().__init__()

        confirm = LineBox(AttrMap(Button("Confirm",
                                         on_press=self.confirm,
                                         align="center"),
                                  "default",
                                  "confirm_button"))

        abort = LineBox(AttrMap(Button("Abort",
                                       on_press=self.quit,
                                       align="center"),
                                "default",
                                "abort_button"))

        grid_elements.append([confirm, abort])

        self.root = Filler(Grid(grid_elements), valign="top")
        self.form = form

    def confirm(self, button):
        try:
            self.form.submit()
            self.quit(button)
        except Exception as e:
            TUI.print(("error", str(e)))

    def quit(self, button):
        TUI.clear()
        self.emit("on_quit", button)
        self.root.base_widget.focus_first()
