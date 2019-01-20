from enum import IntEnum, auto

from urwid import LineBox, RadioButton, Text

from src.views.widgets.grid import Grid


class RadioPolicy(IntEnum):
    HORIZONTAL = auto()
    VERTICAL = auto()


class RadioGroup(Grid):
    def __init__(self, markup, starting_value, enum_type, policy=RadioPolicy.VERTICAL):
        self.selected_value = starting_value
        self.enum_type = enum_type

        self.radio_group = []
        for choice in enum_type:
            RadioButton(self.radio_group,
                        label=choice.name.capitalize(),
                        state=choice is starting_value)

        rows = [
            [Text(markup)]
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
        self._w = LineBox(self._w)

    def get_data(self):
        for radio in self.radio_group:
            if radio.state:
                return self.enum_type[radio.label.upper()]
