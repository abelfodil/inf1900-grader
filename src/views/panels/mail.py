#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from urwid import AttrMap, Columns, Filler, LineBox, Pile, ProgressBar

from src.models.mail import mail
from src.models.state import state
from src.views.base.buffer import Buffer
from src.views.base.button import Button
from src.views.base.controller import Controller
from src.views.base.form import Form
from src.views.base.signal import Signal
from src.views.base.tree import TreeWidget

from src.views.base.tui import TUI


@Signal("on_quit")
class MailPanel(Controller):

    def __init__(self):

        super().__init__()

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

        tree     = TreeWidget(column1)

        tree.split_vertically(column2)
        tree.split_vertically(message)
        tree.split_vertically(buttons_column)

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

        self.root = Pile([Filler(tree, valign="top")])

        self.form = Form(mail,
                         sender_email=sender,
                         recipient_email=recipient,
                         subject=subject,
                         message=message,
                         grading_directory=grading_directory)

    def confirm(self, button):
        try:
            self.form.submit()
            self.emit("on_quit", button)
        except Exception as e:
            TUI.print(str(e))

    def abort(self, button):
        self.emit("on_quit", button)
