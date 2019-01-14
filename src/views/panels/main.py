from urwid import Filler, Text, connect_signal, emit_signal

from src.views.base.signal import Signal, SignalType
from src.views.base.tui import TUI
from src.views.panels.assemble import AssemblePanel
from src.views.panels.clone import ClonePanel
from src.views.panels.grade import GradePanel
from src.views.panels.mail import MailPanel
from src.views.widgets.hydra import HydraWidget


@Signal(SignalType.SWAP)
class MainPanel(HydraWidget):

    def __init__(self):
        super().__init__(info="Welcome to INF1900 interactive grading tool!", align="center")

        self.add_views([
            ("c", "Clone", ClonePanel()),
            ("g", "Grade", GradePanel()),
            ("a", "Assemble", AssemblePanel()),
            ("m", "Mail", MailPanel())
        ])

        self.add_actions([
            ("q", "red_head", "Quit", TUI.quit),
        ])

        self.root = Filler(self, valign="bottom")

    def add_views(self, views):
        heads = []
        for letter, hint, view, in views:
            connect_signal(view, SignalType.QUIT, self.restore)
            heads.append((letter, "blue_head", hint, self.swap_view, {"view": view, "hint": hint}))

        self.add_heads(heads)

    def add_actions(self, actions: list):
        self.add_heads(actions)

    def swap_view(self, view, hint):
        emit_signal(self, SignalType.SWAP, view, hint)

    def restore(self, *kargs):
        self.swap_view(self, "")

    def start_tui(self):
        tui = TUI(self.root, header=Text(("header", ""), "center"))
        connect_signal(self, SignalType.SWAP,
                       lambda view, hint: (tui.body(view.root), tui.print(hint)))

        try:
            tui()
        finally:
            tui.loop.screen.stop()
