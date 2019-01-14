from re import sub

from urwid import LineBox, Pile, RadioButton, Text, WidgetWrap


class RadioGroup(WidgetWrap):
    def __init__(self, enum_type, starting_value):
        self.selected_value = starting_value
        self.enum_type = enum_type

        self.radio_group = []
        for choice in enum_type:
            RadioButton(self.radio_group,
                        label=choice.name.capitalize(),
                        state=choice is starting_value)

        radio_title = sub(r"(\w)([A-Z])", r"\1 \2", enum_type.__name__).capitalize()

        super().__init__(LineBox(Pile([Text(("header", radio_title)), *self.radio_group])))

    def get_data(self):
        for radio in self.radio_group:
            if radio.state:
                return self.enum_type[radio.label.upper()]
