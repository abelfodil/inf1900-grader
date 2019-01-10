#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from urwid import Edit

from src.views.controller import Controller
from src.views.signal     import Signal

@Signal("on_flush")
class Buffer(Edit, Controller):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.kbd = {}

    def keypress(self, size, key):

        if key in self.kbd:
            self.kbd[key]()
            return None

        super().keypress(size, key)


from src.util.dlist import Dlist

@Signal("on_flush")
class MiniBuffer(Buffer):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.history = Dlist("")
        self.current = self.history

        self.kbd = {
            "enter":  self.flush,
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
