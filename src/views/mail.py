if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath("."))

from src.models.mail import *

from src.views.widgets import TreeWidget

from urwid import Edit, Pile, Filler

class MailView:

    instance_n = 0

    def __init__(self):

        # raise exception?
        if MailView.instance_n != 0:
            return
        else:
            MailView.instance_n += 1

        subject  = Edit("Subject  :", f"{default_subject}")
        sender   = Edit("Sender   :", "")
        receiver = Edit("Receiver :", f"{default_receiver}")
        message  = Edit("Message  :", "")

        tree = TreeWidget(subject)
        tree.split_vertically(sender)
        tree.split_vertically(receiver)
        tree.split_vertically(message)


        self.root = Filler(tree)

        self.subject  = subject
        self.sender   = sender
        self.receiver = receiver
        self.message  = message

        self.hint = "Mail"



if __name__ == "__main__":

    from urwid import MainLoop, ExitMainLoop, Filler

    l = MainLoop(Filler(MailView().root))

    l.run()
