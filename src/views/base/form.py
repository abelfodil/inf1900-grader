#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from urwid import Edit, IntEdit, WidgetDecoration

from src.models.state import state

WidgetDecoration.get_data = lambda wrapped_widget: wrapped_widget.base_widget.get_data()
Edit.get_data = Edit.get_edit_text
IntEdit.get_data = IntEdit.value


class Form:

    def __init__(self, on_submit, **kwargs):
        self.on_submit = on_submit
        self.widgets   = kwargs

    def attach(self, name, widget, getter):
        self.widgets.append((name, widget, getter))

    def submit(self):
        data = self.get_data()
        self.on_submit(**data)
        state.override_state(**data)

    def get_data(self):
        return {name: widget.get_data() for name, widget in self.widgets.items()}
