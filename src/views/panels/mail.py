#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from urwid import AttrMap, Columns, Filler, LineBox, Pile, ProgressBar, WidgetPlaceholder

from src.models.state import state
from src.views.base.buffer import Buffer, Controller, Signal
from src.views.base.button import Button
from src.views.base.tree   import TreeWidget


@Signal("on_quit")
class MailPanel(Controller):

    def __init__(self):

        super().__init__()

        subject  = LineBox(Buffer(("header", "Subject\n\n"), state.internal['subject']))

        sender   = LineBox(Buffer(("header", "Sender\n\n"), state.internal["grader_email"]))
        receiver = LineBox(Buffer(("header", "Receiver\n\n"), state.internal["receiver"]))

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

        bar      = ProgressBar("progress_low",
                               "progress_hight",
                               current=10)

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

        self.bar       = Filler(bar, valign="bottom")
        self.hack_pile = Pile([])
        self.subject  = subject
        self.sender   = sender
        self.receiver = receiver
        self.message  = message

        self.root     = Pile([Filler(tree, valign="top"),
                              WidgetPlaceholder(self.hack_pile)])

    # Text from decorator, cuz im lazy
    @staticmethod
    def tfd(d):
        return d.base_widget.get_edit_text()

    def swap_bar(self):
        self.root.contents[1][0].original_widget = self.bar

    def confirm(self, button):
        subject  = MailPanel.tfd(self.subject)
        sender   = MailPanel.tfd(self.sender)
        receiver = MailPanel.tfd(self.receiver)
        message  = MailPanel.tfd(self.message)

        self.swap_bar()

#        mail(sender, receiver, subject, message)

    def abort(self, button):
        self.emit("on_quit", button)
