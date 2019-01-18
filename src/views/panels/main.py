from urwid import Filler, MetaSignals, Text, connect_signal

from src.views.base.signal import SignalType
from src.views.base.tui import TUI
from src.views.panels.assemble import AssemblePanel
from src.views.panels.clone import ClonePanel
from src.views.panels.grade import GradePanel
from src.views.panels.mail import MailPanel
from src.views.widgets.hydra import HydraWidget


class MainPanel(HydraWidget, metaclass=MetaSignals):
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

        self.main_helper_text = self.generate_helper_text([
            ("C-\\", "Close program"),
        ])

        self.subview_helper_text = self.generate_helper_text([
            ("C-\\", "Close program"),
            ("F5", "Confirm"),
            ("F10", "Abort"),
            ("TAB", "Next field"),
            ("S-TAB", "Previous field")
        ])

    def add_views(self, views):
        heads = []
        for letter, hint, view, in views:
            connect_signal(view, SignalType.QUIT, self.display_main)
            heads.append(
                (letter, "blue_head", hint, self.display_subview, {"view": view, "hint": hint}))

        self.add_heads(heads)

    def add_actions(self, actions: list):
        self.add_heads(map(lambda action: (action[0], "red_head", *action[1:]), actions))

    @staticmethod
    def __change_view(view, hint):
        tui = TUI()
        tui.body(view.root)
        tui.print(hint)

    def display_subview(self, view, hint):
        TUI().root.footer = self.subview_helper_text
        self.__change_view(view, hint)

    def display_main(self, *kargs):
        TUI().root.footer = self.main_helper_text
        self.__change_view(self, "")

    @staticmethod
    def generate_helper_text(hints):
        markup = []
        for key, text in hints:
            markup.extend((("helper_key", key), " ", ("helper_text", text), " "))

        return Text(markup, align="center")

    def start_tui(self):
        tui = TUI(self.root, header=Text(("header", ""), "center"), footer=self.main_helper_text)
        try:
            tui()
        finally:
            tui.loop.screen.stop()
