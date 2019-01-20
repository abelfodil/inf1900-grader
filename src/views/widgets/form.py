from collections import Callable
from json import load

from urwid import AttrWrap, Edit, Filler, IntEdit, LineBox, Overlay, Text, WidgetDecoration, \
    WidgetPlaceholder, emit_signal

from src.models.assemble import assemble
from src.models.clone import TeamType, clone
from src.models.grade import AssignmentType, grade
from src.models.mail import mail
from src.models.state import state
from src.views.widgets.button import Button
from src.views.widgets.grid import Grid
from src.views.widgets.radio import RadioGroup

WidgetDecoration.get_data = lambda wrapped_widget: wrapped_widget.base_widget.get_data()
Edit.get_data = Edit.get_edit_text
IntEdit.get_data = IntEdit.value

QUIT_SIGNAL = "quit"
SET_HEADER_TEXT_SIGNAL = "set_header"
DRAW_SIGNAL = "draw"

symbols_list = [
    clone,
    grade,
    assemble,
    mail,
    RadioGroup,
    IntEdit,
    Edit,
    AssignmentType,
    TeamType
]

symbols_dict = {symbol.__name__: symbol for symbol in symbols_list}


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

    @staticmethod
    def parse_from_file(file_path):
        grid_elements = []
        form_entries = {}
        with open(file_path, 'r') as f:
            form = load(f)

        for row in form["inputs"]:
            new_row = []
            for entry in row:
                widget_type = symbols_dict[entry["type"]]
                line_feed = "" if entry["type"] == "RadioGroup" else "\n\n"
                markup = ("header", f"{entry['description']}{line_feed}")

                enum = {"enum_type": symbols_dict[entry["enum"]]} if "enum" in entry else {}
                multiline = {"multiline": entry["multiline"]} if "multiline" in entry else {}

                widget = LineBox(widget_type(
                    markup,
                    state.__dict__[entry["name"]],
                    **enum,
                    **multiline
                ))

                new_row.append(widget)
                form_entries[entry["name"]] = widget

            grid_elements.append(new_row)

        return (
            form["keybind"],
            Form(form["name"], grid_elements, form_entries, symbols_dict[form["callback"]])
        )
