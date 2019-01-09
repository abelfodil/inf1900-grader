# Olivier Dion - 2019

from src.models.mail   import *
from src.views.widgets import TreeWidget, Buffer, Button

from src.views.tui     import TUI

from urwid import (
    AttrMap,
    Columns,
    Edit,
    Filler,
    Frame,
    LineBox,
    ListBox,
    Pile,
    ProgressBar,
    WidgetContainerMixin,
    WidgetDecoration
)

from time import sleep

class MailView:

    def __init__(self):

        subject  = LineBox(Buffer(("header", "Subject\n\n"), f"{default_subject}"))

        sender   = LineBox(Buffer(("header", "Sender\n\n"), ""))
        receiver = LineBox(Buffer(("header", "Receiver\n\n"), f"{debug_receiver}"))

        infos    = Columns([sender, receiver])

        message  = LineBox(Buffer(("header" ,"Message\n\n"), "", multiline=True))

        confirm  = LineBox(AttrMap(Button("Confirm",
                                          on_press=self.confirm,
                                          align="center"),
                                   "default",
                                   "confirm_button"))

        abort    = LineBox(AttrMap(Button("Abort",
                                          on_press=self.abort,
                                          align="center"),
                                   "default",
                                   "abort_button"))

        buttons  = Columns([confirm, abort])

        tree     = TreeWidget(subject)

        tree.split_vertically(infos)
        tree.split_vertically(message)
        tree.split_vertically(buttons)

        tree.bind("up",  tree.focus_prev_node)
        tree.bind("down",tree.focus_next_node)

        tree.set_aliases(
            [
                ("ctrl p",    "up"),
                ("shift tab", "up"),
                ("ctrl n",    "down"),
                ("tab",       "down"),
                ("ctrl f",    "right"),
                ("ctrl b",    "left"),
            ]
        )

        bar = ProgressBar("default", "confirm_button", current=50)

        self.root     = Pile([Filler(tree), Filler(bar)])
        self.bar      = bar
        self.subject  = subject
        self.sender   = sender
        self.receiver = receiver
        self.message  = message

    # Text from decorator, cuz im lazy
    @staticmethod
    def tfd(d):
        return d.base_widget.get_edit_text()

    def confirm(self, button):
        subject  = MailView.tfd(self.subject)
        sender   = MailView.tfd(self.sender)
        receiver = MailView.tfd(self.receiver)
        message  = MailView.tfd(self.message)

        self.bar.set_completion(100)

#        mail(sender, receiver, subject, message)









    def abort(self, button):
        TUI.quit()
