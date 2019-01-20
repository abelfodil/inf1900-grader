from collections import Callable

from urwid import AttrWrap, Edit, Filler, IntEdit, Overlay, Text, WidgetDecoration, \
    WidgetPlaceholder, emit_signal

from src.models.state import state
from src.views.base.tui import TUI
from src.views.widgets.button import Button
from src.views.widgets.grid import Grid

WidgetDecoration.get_data = lambda wrapped_widget: wrapped_widget.base_widget.get_data()
Edit.get_data = Edit.get_edit_text
IntEdit.get_data = IntEdit.value

QUIT_SIGNAL = "on_quit"


class Form(Grid):
    signals = [QUIT_SIGNAL]

    def __init__(self, name, named_grid_elements: list, callback: Callable):
        self.name = name
        self.named_widgets = {}
        unnamed_grid_elements = []
        for row in named_grid_elements:
            self.named_widgets.update(row)
            unnamed_grid_elements.append(list(row.values()))

        confirm = Button("Confirm", "confirm_button", self.__confirm)
        abort = Button("Abort", "abort_button", self.__quit)
        unnamed_grid_elements.append([confirm, abort])

        super().__init__(unnamed_grid_elements)
        self.keybind["f1"] = self.__confirm
        self.keybind["f5"] = self.__quit

        self.on_submit = callback

        bottom = Filler(self, valign="top")
        popup = AttrWrap(Filler(Text("Work in progress...\n\nPlease wait.", "center")), "popup")
        self.overlay = Overlay(popup, bottom, "center", 30, "middle", 5)

        self.root = WidgetPlaceholder(bottom)

    def render_form(self):
        self.root.original_widget = self.overlay.bottom_w
        TUI().loop.draw_screen()

    def render_overlay(self):
        self.root.original_widget = self.overlay
        TUI().loop.draw_screen()

    def __confirm(self):
        TUI().set_header_text(self.name)
        self.render_overlay()

        try:
            self.__submit()
            self.__quit()
        except Exception as e:
            TUI().set_header_text(("error", str(e)))
        finally:
            self.render_form()

    def __quit(self):
        TUI().set_header_text(self.name)
        emit_signal(self, QUIT_SIGNAL)
        self.overlay.bottom_w.base_widget.focus_first()

    def __submit(self):
        data = self.__get_form_data()
        self.on_submit(**data)
        state.override_state(**data)

    def __get_form_data(self):
        return {name: widget.get_data() for name, widget in self.named_widgets.items()}
