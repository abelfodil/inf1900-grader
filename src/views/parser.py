from json import load
from os import listdir
from os.path import dirname, join, realpath

from urwid import Edit, IntEdit, LineBox, WidgetDecoration

from src.models.assemble import assemble
from src.models.clone import TeamType, clone
from src.models.grade import AssignmentType, grade
from src.models.mail import mail
from src.models.state import state
from src.views.widgets.form import Form
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


def parse_row_entry(entry):
    is_radio = entry["type"] == "RadioGroup"

    line_feed = "" if is_radio else "\n\n"
    markup = ("header", f"{entry['description']}{line_feed}")
    enum = {"enum_type": symbols_dict[entry["enum"]]} if "enum" in entry else {}
    multiline = {"multiline": entry["multiline"]} if "multiline" in entry else {}

    widget_type = symbols_dict[entry["type"]]
    widget = widget_type(
        markup,
        state.__dict__[entry["name"]],
        **enum,
        **multiline
    )

    return widget if is_radio else LineBox(widget)


def parse_form_from_file(file_path):
    with open(file_path, 'r') as f:
        form = load(f)

    grid_elements = []
    form_entries = {}

    for row in form["inputs"]:
        new_row = []
        for entry in row:
            widget = parse_row_entry(entry)
            new_row.append(widget)
            form_entries[entry["name"]] = widget

        grid_elements.append(new_row)

    return (
        form["keybind"],
        Form(form["name"], grid_elements, form_entries, symbols_dict[form["callback"]])
    )


def parse_forms():
    forms_path = f"{dirname(realpath(__file__))}/forms"
    for file_path in sorted(listdir(forms_path)):
        yield parse_form_from_file(join(forms_path, file_path))
