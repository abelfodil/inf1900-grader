#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from urwid import AttrMap, Columns, Filler, LineBox, Pile, ProgressBar, WidgetPlaceholder

from src.models.state import state
from src.views.base.buffer import Buffer, Controller, Signal
from src.views.base.button import Button
from src.views.base.tree import TreeWidget


def get_edit_text(self):
    return self.base_widget.get_edit_text()


LineBox.get_value = get_edit_text

@Signal("on_quit")
class MailPanel(Controller):

    def __init__(self):

        super().__init__()

        sender   = LineBox(Buffer(("header", "Sender\n\n"), state.grader_email))
        receiver = LineBox(Buffer(("header", "Receiver\n\n"), state.recipient))
        column1  = Columns([sender, receiver])

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

        self.bar       = Filler(bar, valign="bottom")
        self.hack_pile = Pile([])
        self.subject  = subject
        self.sender   = sender
        self.receiver = receiver
        self.message  = message

        self.root     = Pile([Filler(tree, valign="top"),
                              WidgetPlaceholder(self.hack_pile)])

    def swap_bar(self):
        self.root.contents[1][0].original_widget = self.bar

    def confirm(self, button):
        subject  = self.subject.get_value()
        sender   = self.sender.get_value()
        receiver = self.receiver.get_value()
        message  = self.message.get_value()

        self.swap_bar()

#        mail(sender, receiver, subject, message)

    def abort(self, button):
        self.emit("on_quit", button)
