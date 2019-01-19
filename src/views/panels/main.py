from urwid import Filler, Text, connect_signal

from src.views.base.tui import TUI
from src.views.panels.assemble import AssemblePanel
from src.views.panels.clone import ClonePanel
from src.views.panels.grade import GradePanel
from src.views.panels.mail import MailPanel
from src.views.widgets.form import QUIT_SIGNAL
from src.views.widgets.hydra import HydraWidget


class MainPanel(HydraWidget):
    def __init__(self):
        super().__init__(info="Welcome to INF1900 interactive grading tool!", align="center")

        self.add_views([
            ("c", "Clone", ClonePanel()),
            ("g", "Grade", GradePanel()),
            ("a", "Assemble", AssemblePanel()),
            ("m", "Mail", MailPanel())
        ])

        self.root = Filler(self, valign="middle")

        self.main_helper_text = self.generate_helper_text([
            ("F10", "Quit", "helper_text_red"),
        ])

        self.subview_helper_text = self.generate_helper_text([
            ("F1", "Confirm", "helper_text_green"),
            ("F5", "Abort", "helper_text_brown"),
            ("F10", "Quit", "helper_text_red"),
            ("TAB", "Next", "helper_text_light"),
            ("S-TAB", "Previous", "helper_text_light")
        ])

    def add_views(self, views):
        heads = []
        for letter, hint, view, in views:
            connect_signal(view, QUIT_SIGNAL, self.display_main)
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
        for key, text, text_palette in hints:
            markup.extend((("helper_key", key), " ", (text_palette, text), " "))

        return Text(markup, align="center")

    def start_tui(self):
        tui = TUI(self.root, header=Text(("header", ""), "center"), footer=self.main_helper_text)
        tui.bind_global("f10", tui.quit)

        try:
            tui()
        finally:
            tui.loop.screen.stop()
