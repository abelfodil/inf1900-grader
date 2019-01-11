#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from urwid import AttrMap, Columns, LineBox, ProgressBar

from src.models.mail import mail
from src.models.state import state
from src.views.base.buffer import Buffer
from src.views.base.button import Button
from src.views.base.form import Form
from src.views.base.signal import Signal
from src.views.panels.abstract import AbstractPanel


@Signal("on_quit")
class ClonePanel(AbstractPanel):

    def __init__(self):
        sender    = LineBox(Buffer(("header", "Sender email\n\n"), state.sender_email))
        recipient = LineBox(Buffer(("header", "Recipient email\n\n"), state.recipient_email))
        column1   = Columns([sender, recipient])

        grading_directory = LineBox(Buffer(("header", "Grading directory\n\n"), state.grading_directory))
        subject  = LineBox(Buffer(("header", "Subject\n\n"), state.subject))
        column2  = Columns([grading_directory, subject])

        message  = LineBox(Buffer(("header" ,"Message\n\n"), state.message, multiline=True))

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

        buttons_column  = Columns([confirm, abort])

        bar      = ProgressBar("progress_low",
                               "progress_hight",
                               current=10)

        form = Form(mail,
                    sender_email=sender,
                    recipient_email=recipient,
                    subject=subject,
                    message=message,
                    grading_directory=grading_directory)

        super().__init__(column1, form)
        self.tree.split_vertically(column2)
        self.tree.split_vertically(message)
        self.tree.split_vertically(buttons_column)
