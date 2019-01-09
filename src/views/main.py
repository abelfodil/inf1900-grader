# Olivier Dion - 2019

from src.views.widgets import HydraWidget, Signal, Controller
from src.views.hydra   import Hydra

from urwid import Filler

@Signal("on_swap")
class MainView(HydraWidget, Controller):

    def __init__(self):

        hydra = Hydra("MainView", [],
                      info="Welcome to INF1900 interactive grading tool!",
                      color=Hydra.blue)

        super().__init__(hydra=hydra, align="center")

        self.body = Filler(self, valign="bottom")

    def add_views(self, views):

        if not isinstance(views, list):
            views = [views]

        heads = []

        for view in views:
            heads.append((view[0], lambda: self.swap_view(view[1]), view[2]))

        self.add_heads(heads)

    def add_actions(self, actions):

        if not isinstance(actions, list):
            actions = [actions]

        heads = []

        for action in actions:
            heads.append((action[0], action[1], action[2]))

        self.add_heads(heads)

    def swap_view(self, view):
        self.emit("on_swap", view.root)

    def restore(self, *kargs):
        self.emit("on_swap", self.body)
