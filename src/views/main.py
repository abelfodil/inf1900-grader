from src.views.widgets import HydraWidget

from src.views.hydra import HydraHead, Hydra

from urwid import Filler

class MainView:

    def __init__(self):

        self.hydra = HydraWidget(Hydra("main_hydra", [], color=Hydra.blue))
        self.root = Filler(self.hydra, valign="bottom")

        self.views = {}

        self.stack_views = []

    def add_view(self, bind, view):
        if bind in self.views:
            self.remove_view(bind)

        self.views[bind] = view

        heads = [(bind, lambda: self.swap_view(view.root), view.hint)]

        self.hydra.add_heads(heads)

    def remove_view(self, bind):
        del self.views[bind]
