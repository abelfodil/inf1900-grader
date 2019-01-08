#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

import urwid

from hydra   import Hydra
from widgets import TreeWidget, HydraWidget

# +------------------------------+
# | Echo screen...               |
# |                              |
# |                              |
# |                              |
# |                              |
# |                              |
# |                              |
# |==============================|
# |         Hydra info           |
# |                              |
# |  [h], [e], [a], [d], [s]     |
# |------------------------------|
# | > mini buffer                |
# +------------------------------+

# +=====================================================+
# |+-: root (box) -------------------------------------+|
# ||+-: header (flow) --------------------------------+||
# |||                                                 |||
# ||+-------------------------------------------------+||
# ||+-: body (box) -----------------------------------+||
# |||                                                 |||
# |||                                                 |||
# |||                                                 |||
# |||                                                 |||
# |||                                                 |||
# |||                                                 |||
# |||                                                 |||
# |||                                                 |||
# |||                                                 |||
# |||                                                 |||
# ||+-------------------------------------------------+||
# ||+-: mini buff (flow) -----------------------------+||
# |||                                                 | |
# ||+-------------------------------------------------+||
# |+---------------------------------------------------+|
# +=====================================================+


class TUIException(Exception):

    def __init__(msg, *kargs, **kwargs):
        super().__init__(msg, *kargs, **kwargs)

class TUI:

    palette = [
        ("blue_head", "dark blue", ""),
        ("red_head", "dark red", "")
    ]


    def __init__(self, body, header=None, footer=None):

        self.root      = urwid.Frame(body,
                                     header,
                                     footer)

        self.loop = urwid.MainLoop(self.root, TUI.palette,
                                   unhandled_input=self.unhandled_input)

        self.globals_kbd = {}

    def __call__(self):
        self.loop.run()

    def focus_header(self):
        self.root.focus_position = "header"

    def focus_body(self):
        self.root.focus_position = "body"

    def focus_footer(self):
        self.root.focus_position = "footer"

    def header(self, flow_widget=None):

        if flow_widget is not None:
            if "flow" not in flow_widget.sizing():
                raise TUIException("Header must be of sizing flow")

            self.root.contents["header"] = flow_widget

        return self.root.contents["header"]

    def body(self, box_widget=None):

        if box_widget is not None:
            if "box" not in flow_widget.sizing():
                raise TUIException("Body must be of sizing box")

            self.root.contents["body"] = flow_widget

        return self.root.contents["body"]

    def footer(self, flow_widget=None):

        if flow_widget is not None:
            if "flow" not in flow_widget.sizing():
                raise TUIException("Header must be of sizing flow")

            self.root.contents["footer"] = flow_widget

        return self.root.contents["footer"]

    def unhandled_input(self, key):

        if key in self.globals_kbd:
            self.globals_kbd[key]()

    def bind_global(self, key, callback):
        self.globals_kbd[key] = callback

    @staticmethod
    def quit():
        raise urwid.ExitMainLoop()


if __name__ == "__main__":

    from urwid import LineBox, Filler

    heads = [
        ('g', None, "", False),
        ('H', None, "Hint"),
        ('q', TUI.quit, "quit")
    ]

    menu_hydra = Hydra("Test", heads, "infos", Hydra.blue)

    hydra_w = HydraWidget(menu_hydra, align="center")

    tui = TUI(TreeWidget(Filler(LineBox(hydra_w),  valign="bottom")),
              footer=None)

    tui()
