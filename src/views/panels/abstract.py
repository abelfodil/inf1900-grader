from urwid import AttrMap, Filler, LineBox, MetaSignals, emit_signal

from src.views.base.form import Form
from src.views.base.signal import SignalType
from src.views.base.tui import TUI
from src.views.widgets.button import Button
from src.views.widgets.grid import Grid


class AbstractPanel(metaclass=MetaSignals):
    signals = [SignalType.QUIT]

    def __init__(self, grid_elements: list, form: Form):

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
        emit_signal(self, SignalType.QUIT, button)
        self.root.base_widget.focus_first()
