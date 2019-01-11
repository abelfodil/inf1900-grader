#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from urwid import Edit, IntEdit, LineBox, Pile, RadioButton

from src.util.dlist import Dlist
from src.views.base.controller import Controller
from src.views.base.signal import Signal


@Signal("on_flush")
class EditBuffer(Edit, Controller):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@Signal("on_flush")
class IntEditBuffer(IntEdit, Controller):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@Signal("on_flush")
class RadioBuffer(Controller):
    def __init__(self, radios):
        super().__init__()

        self.selected_value = radios[0][1]

        radio_group = []
        for radio in radios:
            RadioButton(radio_group, radio[0],
                        on_state_change=self.__set_selected_value,
                        user_data=radio[1])

        self.wrap = LineBox(Pile(radio_group))

    def __set_selected_value(self, **kwargs):
        self.selected_value = kwargs["user_data"]

    def get_data(self):
        return self.selected_value


@Signal("on_flush")
class MiniBuffer(EditBuffer):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.history = Dlist("")
        self.current = self.history

        self.keybind = {
            "enter" : self.flush,
            "ctrl p": self.previous_history,
            "ctrl n": self.next_history,
            "ctrl r": self.reverse_i_search
        }

    def flush(self):

        txt = self.get_edit_text()

        if txt != self.current.prev.data:
            self.current.data = txt
            self.current.add(Dlist(""))
            self.current = self.current.next
        else:
            self.current.data = ""

        self.history = self.current

        self.set_edit_text("")

        self.emit("on_flush", self.get_last_text())

    def previous_history(self):
        self.history.data = self.get_edit_text()
        self.history = self.history.prev
        self.update_text(self.history.data)

    def next_history(self):
        self.history.data = self.get_edit_text()
        self.history = self.history.next
        self.update_text(self.history.data)

    def reverse_i_search(self):
        pass

    def update_text(self, text):
        self.set_edit_text(text)
        self.set_edit_pos(len(text))

    def get_last_text(self):
        return self.current.prev.data
