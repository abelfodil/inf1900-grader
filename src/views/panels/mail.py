#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from urwid import Columns, LineBox, GridFlow, Filler, AttrMap
from src.models.mail           import mail
from src.models.state          import state
from src.views.base.buffer     import EditBuffer
from src.views.base.button     import Button
from src.views.base.form       import Form
from src.views.base.grid       import Grid
from src.views.panels.abstract import AbstractPanel
from src.views.base.signal     import Signal

@Signal("on_quit")
class MailPanel(AbstractPanel):

    def __init__(self):

        sender    = LineBox(EditBuffer(("header", "Sender email\n\n"),
                                       state.sender_email))

        recipient = LineBox(EditBuffer(("header", "Recipient email\n\n"),
                                       state.recipient_email))

        grading_directory = LineBox(EditBuffer(("header", "Grading directory\n\n"),
                                               state.grading_directory))

        subject  = LineBox(EditBuffer(("header", "Subject\n\n"),
                                      state.subject))

        message  = LineBox(EditBuffer(("header" , "Message\n\n"),
                                      state.message, multiline=True))

        form = Form(mail,
                    sender_email=sender,
                    recipient_email=recipient,
                    subject=subject,
                    message=message,
                    grading_directory=grading_directory)

        super().__init__(form)

        grid = Grid([
            [sender, recipient],
            [grading_directory, subject],
            [message],
            self.buttons      # from parent
        ])

        grid.bind([
            ("up", lambda:grid.focus_vertical(-1)),
            ("down", lambda:grid.focus_vertical(1)),
            ("tab", grid.focus_next),
            ("shift tab", grid.focus_prev)
        ])

        grid.set_aliases([
            ("ctrl f", "left"),
            ("ctrl b", "right"),
            ("ctrl p", "up"),
            ("ctrl n", "down")
        ])

        self.root = Filler(grid, valign="top")
