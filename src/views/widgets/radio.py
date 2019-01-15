from re import sub
from enum import IntEnum, auto

from urwid import LineBox, Pile, RadioButton, Text, WidgetWrap

from src.views.widgets.grid import Grid

class RadioPolicy:
    HORIZONTAL = auto()
    VERTICAL   = auto()


class RadioGroup(Grid):
    def __init__(self, enum_type, starting_value, policy=RadioPolicy.VERTICAL):
        self.selected_value = starting_value
        self.enum_type = enum_type

        self.radio_group = []
        for choice in enum_type:
            RadioButton(self.radio_group,
                        label=choice.name.capitalize(),
                        state=choice is starting_value)

        radio_title = sub(r"(\w)([A-Z])", r"\1 \2", enum_type.__name__).capitalize()

        rows = [
            [Text(("header", radio_title))]
        ]

        if policy is RadioPolicy.VERTICAL:
            for radio in self.radio_group:
                rows.append([radio])
        else:
            col = []
            for radio in self.radio_group:
                col.append(radio)
            rows.append(col)

        super().__init__(rows)

    def get_data(self):
        for radio in self.radio_group:
            if radio.state:
                return self.enum_type[radio.label.upper()]
