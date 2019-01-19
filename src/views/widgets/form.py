from collections import Callable

from urwid import Edit, Filler, IntEdit, WidgetDecoration, emit_signal

from src.models.state import state
from src.views.base.signal import SignalType
from src.views.base.tui import TUI
from src.views.widgets.button import Button
from src.views.widgets.grid import Grid

WidgetDecoration.get_data = lambda wrapped_widget: wrapped_widget.base_widget.get_data()
Edit.get_data = Edit.get_edit_text
IntEdit.get_data = IntEdit.value


class Form(Grid):
    signals = [SignalType.QUIT]

    def __init__(self, named_grid_elements: list, callback: Callable):
        self.named_widgets = {}
        unnamed_grid_elements = []
        for row in named_grid_elements:
            self.named_widgets.update(row)
            unnamed_grid_elements.append(list(row.values()))

        confirm = Button("Confirm", "confirm_button", self.__confirm)
        abort = Button("Abort", "abort_button", self.__quit)
        unnamed_grid_elements.append([confirm, abort])

        super().__init__(unnamed_grid_elements)
        self.root = Filler(self, valign="top")

        self.keybinds["f5"] = self.__confirm
        self.keybinds["f10"] = self.__quit
        self.on_submit = callback

    def __confirm(self):
        try:
            self.__submit()
            self.__quit()
        except Exception as e:
            TUI.print(("error", str(e)))

    def __quit(self):
        TUI.clear()
        emit_signal(self, SignalType.QUIT)
        self.root.base_widget.focus_first()

    def __submit(self):
        data = self.__get_form_data()
        self.on_submit(**data)
        state.override_state(**data)

    def __get_form_data(self):
        return {name: widget.get_data() for name, widget in self.named_widgets.items()}
