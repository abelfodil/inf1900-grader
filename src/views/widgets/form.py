from collections import Callable

from urwid import AttrMap, Edit, Filler, IntEdit, LineBox, MetaSignals, WidgetDecoration, \
    emit_signal

from src.models.state import state
from src.views.base.signal import SignalType
from src.views.base.tui import TUI
from src.views.widgets.button import Button
from src.views.widgets.grid import Grid

WidgetDecoration.get_data = lambda wrapped_widget: wrapped_widget.base_widget.get_data()
Edit.get_data = Edit.get_edit_text
IntEdit.get_data = IntEdit.value


class Form(Grid, metaclass=MetaSignals):
    signals = [SignalType.QUIT]

    def __init__(self, named_grid_elements: list, callback: Callable):

        confirm = LineBox(AttrMap(Button("Confirm", on_press=self.__confirm, align="center"),
                                  "default",
                                  "confirm_button"))

        abort = LineBox(AttrMap(Button("Abort", on_press=self.__quit, align="center"),
                                "default",
                                "abort_button"))

        self.named_widgets = {}
        unnamed_grid_elements = []
        for row in named_grid_elements:
            self.named_widgets.update(row)
            unnamed_grid_elements.append(list(row.values()))

        unnamed_grid_elements.append([confirm, abort])

        super().__init__(unnamed_grid_elements)

        self.root = Filler(self, valign="top")
        self.on_submit = callback

    def __confirm(self, button):
        try:
            self.__submit()
            self.__quit(button)
        except Exception as e:
            TUI.print(("error", str(e)))

    def __quit(self, button):
        TUI.clear()
        emit_signal(self, SignalType.QUIT, button)
        self.root.base_widget.focus_first()

    def __submit(self):
        data = self.__get_form_data()
        self.on_submit(**data)
        state.override_state(**data)

    def __get_form_data(self):
        return {name: widget.get_data() for name, widget in self.named_widgets.items()}
