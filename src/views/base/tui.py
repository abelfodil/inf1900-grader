#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

import os
import signal
import sys

from urwid import ExitMainLoop, Frame, MainLoop


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
    # TODO: add static method to add palette from view
    palette = [
        ("blue_head", "dark blue", ""),
        ("red_head", "dark red", ""),
        ("header", "bold, underline", ""),
        ("normal_box", "default", "default"),
        ("selected_box", "black", "light gray"),
        ("confirm_button", "light cyan", "dark green"),
        ("abort_button", "light red", "brown"),
        ("progress_low", "default", "yellow"),
        ("progress_hight", "default", "dark green"),
    ]

    keybind = {}

    singleton = None

    def __init__(self, body, header=None, footer=None):

        if TUI.singleton is not None:
            raise Exception("More than one singleton instance")

        self.root = Frame(body,
                          header,
                          footer)

        TUI.loop = MainLoop(self.root, TUI.palette,
                            unhandled_input=self.unhandled_input)

        TUI.install_signals_handler()

        TUI.singleton = self

    def __call__(self):
        TUI.loop.run()

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
            if "box" not in box_widget.sizing():
                raise TUIException("Body must be of sizing box")

            self.root.contents["body"] = (box_widget, self.root.options())

        return self.root.contents["body"]

    def footer(self, flow_widget=None):

        if flow_widget is not None:
            if "flow" not in flow_widget.sizing():
                raise TUIException("Header must be of sizing flow")

            self.root.contents["footer"] = flow_widget

        return self.root.contents["footer"]

    def unhandled_input(self, key):
        if key in TUI.keybind:
            TUI.keybind[key]()

    def bind_global(self, key, callback):
        TUI.keybind[key] = callback


    @classmethod
    def print(cls, string):
        cls.singleton.print(string)

    @staticmethod
    def quit(*kargs):
        raise ExitMainLoop()

    @staticmethod
    def pause(*kargs):
        print("PAUSE")
        TUI.loop.stop()
        os.kill(os.getpid(), signal.SIGSTOP)
        TUI.loop.start()
        TUI.loop.draw_screen()

    @staticmethod
    def interrupt(*kargs):
        pass

    @staticmethod
    def install_signals_handler():

        if sys.platform != "win32":
            signal.signal(signal.SIGQUIT, TUI.quit)
            signal.signal(signal.SIGTSTP, TUI.pause)

        ###############################################################
        # TODO Windows:                                               #
        #                                                             #
        # sys.platform == win32 Should test for                       #
        # signal.CTRL_BREAK_EVENT and signal.CTRL_C_EVENT and hook to #
        # appropriate callback                                        #
        ###############################################################

        signal.signal(signal.SIGINT, TUI.interrupt)
