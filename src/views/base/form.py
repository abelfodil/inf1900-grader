#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from urwid import Edit, WidgetDecoration


def unwrap_data(wrapped_widget):
    return wrapped_widget.base_widget.get_data()


WidgetDecoration.get_data = unwrap_data
Edit.get_data = Edit.get_edit_text


class Form:

    def __init__(self, on_submit, **kwargs):
        self.on_submit = on_submit
        self.widgets   = kwargs

    def attach(self, name, widget, getter):
        self.widgets.append((name, widget, getter))

    def submit(self):
        data = {}

        for name, widget in self.widgets.items():
            data[name] = widget.get_data()

        self.on_submit(**data)
