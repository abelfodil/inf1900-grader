from collections import Callable

from urwid import AttrWrap, Edit, Filler, IntEdit, Overlay, Text, WidgetDecoration, \
    WidgetPlaceholder, emit_signal

from src.models.state import state
from src.views.widgets.button import Button
from src.views.widgets.grid import Grid

WidgetDecoration.get_data = lambda wrapped_widget: wrapped_widget.base_widget.get_data()
Edit.get_data = Edit.get_edit_text
IntEdit.get_data = IntEdit.value

QUIT_SIGNAL = "quit"
SET_HEADER_TEXT_SIGNAL = "set_header"
DRAW_SIGNAL = "draw"


class Form(Grid):
    signals = [QUIT_SIGNAL, SET_HEADER_TEXT_SIGNAL, DRAW_SIGNAL]

    def __init__(self, name, grid_elements: list, form_entries: dict, callback: Callable):
        confirm = Button("Confirm", "confirm_button", self.__confirm)
        abort = Button("Abort", "abort_button", self.__quit)
        grid_elements.append([confirm, abort])
        super().__init__(grid_elements)
        self.form_entries = form_entries

        self.name = name
        self.keybind["f1"] = self.__confirm
        self.keybind["f5"] = self.__quit

        self.on_submit = callback

        bottom = Filler(self, valign="top")
        popup = AttrWrap(Filler(Text("Work in progress...\n\nPlease wait.", "center")), "popup")
        self.overlay = Overlay(popup, bottom, "center", 30, "middle", 5)

        self.root = WidgetPlaceholder(bottom)

    def render_form(self):
        self.root.original_widget = self.overlay.bottom_w
        emit_signal(self, DRAW_SIGNAL)

    def render_overlay(self):
        self.root.original_widget = self.overlay
        emit_signal(self, DRAW_SIGNAL)

    def __confirm(self):
        emit_signal(self, SET_HEADER_TEXT_SIGNAL, self.name)
        self.render_overlay()

        try:
            self.__submit()
            self.__quit()
        except Exception as e:
            emit_signal(self, SET_HEADER_TEXT_SIGNAL, ("error", str(e)))
        finally:
            self.render_form()

    def __quit(self):
        emit_signal(self, SET_HEADER_TEXT_SIGNAL, self.name)
        emit_signal(self, QUIT_SIGNAL)
        self.overlay.bottom_w.base_widget.focus_first()

    def __submit(self):
        data = self.__get_form_data()
        self.on_submit(**data)
        state.override_state(**data)

    def __get_form_data(self):
        return {name: widget.get_data() for name, widget in self.form_entries.items()}
