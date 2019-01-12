#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from urwid import Filler

from src.views.base.buffer import Controller, Signal
from src.views.base.hydra import Hydra, HydraWidget
from src.views.base.tui import TUI
from src.views.panels.assemble import AssemblePanel
from src.views.panels.clone import ClonePanel
from src.views.panels.grade import GradePanel
from src.views.panels.mail import MailPanel


@Signal("on_swap")
class MainPanel(HydraWidget, Controller):

    def __init__(self):
        hydra = Hydra("MainView", [],
                      info="Welcome to INF1900 interactive grading tool!",
                      color=Hydra.blue)

        super().__init__(hydra=hydra, align="center")

        views = [
            ("c", ClonePanel(), "Clone"),
            ("g", GradePanel(), "Grade"),
            ("a", AssemblePanel(), "Assemble"),
            ("m", MailPanel(), "Mail")
        ]

        self.add_views(views)

        self.root = Filler(self, valign="bottom")

        self.add_actions(
            [
                ("q", TUI.quit, "Quit"),
            ]
        )

    def add_views(self, views):

        heads = []

        for letter, view, hint, in views:
            view.connect("on_quit", self.restore)
            heads.append((letter, self.swap_view, hint, None, {"view": view,
                                                               "hint": hint}))

        self.add_heads(heads)

    def add_actions(self, actions):

        if not isinstance(actions, list):
            actions = [actions]

        heads = []

        for action in actions:
            heads.append((action[0], action[1], action[2]))

        self.add_heads(heads)

    def swap_view(self, view, hint):
        self.emit("on_swap", view, hint)

    def restore(self, *kargs):
        self.emit("on_swap", self, "")
