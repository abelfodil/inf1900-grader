if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath("."))

from src.models.mail import *

from src.views.widgets import TreeWidget

from urwid import (
    Button,
    Columns,
    Edit,
    Filler,
    LineBox,
    ListBox,
    Pile,
    WidgetContainerMixin,
    WidgetDecoration
)

class MailView:

    def __init__(self):

        subject  = LineBox(Edit(("header", "Subject\n\n"), f"{default_subject}"))

        sender   = LineBox(Edit(("header", "Sender\n\n"), ""))
        receiver = LineBox(Edit(("header", "Receiver\n\n"), f"{default_receiver}"))

        infos    = Columns([sender, receiver])

        message  = LineBox(Edit(("header" ,"Message\n\n"), "", multiline=True))

        confirm = LineBox(Button("Confirm"))
        abort   = LineBox(Button("Abort"))

        buttons  = Columns([confirm, abort])

        tree = TreeWidget(subject)

        tree.split_vertically(infos)
        tree.split_vertically(message)
        tree.split_vertically(buttons)

        tree.bind("up",  tree.focus_prev_node)
        tree.bind("down",tree.focus_next_node)

        tree.set_aliases(
            [
                ("ctrl p",    "up"),
                ("shift tab", "up")
                ("ctrl n",    "down"),
                ("tab",       "down"),
                ("ctrl f",    "right"),
                ("ctrl b",    "left"),
            ]
        )

        self.root = Filler(tree)

        self.subject  = subject
        self.sender   = sender
        self.receiver = receiver
        self.message  = message




if __name__ == "__main__":

    from urwid import MainLoop, ExitMainLoop, Filler

    l = MainLoop(Filler(MailView().root))

    l.run()
