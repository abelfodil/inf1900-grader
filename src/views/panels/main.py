from urwid import Filler, MetaSignals, Text, connect_signal, emit_signal

from src.views.base.signal import SignalType
from src.views.base.tui import TUI
from src.views.panels.assemble import AssemblePanel
from src.views.panels.clone import ClonePanel
from src.views.panels.grade import GradePanel
from src.views.panels.mail import MailPanel
from src.views.widgets.hydra import HydraWidget


class MainPanel(HydraWidget, metaclass=MetaSignals):
    signals = [SignalType.SWAP]

    def __init__(self):
        super().__init__(info="Welcome to INF1900 interactive grading tool!", align="center")

        self.add_views([
            ("c", "Clone", ClonePanel()),
            ("g", "Grade", GradePanel()),
            ("a", "Assemble", AssemblePanel()),
            ("m", "Mail", MailPanel())
        ])

        self.add_actions([
            ("q", "Quit", TUI.quit),
        ])

        self.root = Filler(self, valign="middle")


    def add_views(self, views):
        heads = []
        for letter, hint, view, in views:
            connect_signal(view, SignalType.QUIT, self.restore)
            heads.append((letter, "blue_head", hint, self.swap_view, {"view": view, "hint": hint}))

        self.add_heads(heads)

    def add_actions(self, actions: list):
        self.add_heads(map(lambda action: (action[0], "red_head", *action[1:]), actions))

    def swap_view(self, view, hint):
        emit_signal(self, SignalType.SWAP, view, hint)

    def restore(self, *kargs):
        self.swap_view(self, "")

    def start_tui(self):

        helper = [
            ("C-p", "Next vertical"),
            ("C-n", "Prev vertical"),
            ("C-f", "Forward char"),
            ("C-b", "Backward char"),
            ("TAB", "Next horizontal"),
            ("S-TAB", "Prev horizontal")
        ]

        # Glitch
        markup = ["\n"]

        for key, text in helper:
            markup.append(("helper_key", key))
            markup.append(" ")
            markup.append(("helper_text", text))
            markup.append(" ")

        helper_text = Text(markup, align="center")

        tui = TUI(self.root, header=Text(("header", ""), "center"), footer=helper_text)
        connect_signal(self, SignalType.SWAP,
                       lambda view, hint: (tui.body(view.root), tui.print(hint)))

        try:
            tui()
        finally:
            tui.loop.screen.stop()
