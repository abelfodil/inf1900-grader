import os
import signal
import sys

from urwid import ExitMainLoop, Frame, MainLoop, Text

from src.util.singleton import Singleton


class TUI(metaclass=Singleton):
    palette = (
        ("blue_head", "dark blue", ""),
        ("red_head", "dark red", ""),
        ("header", "bold, underline, brown", ""),
        ("error", "bold, light red", ""),
        ("normal_box", "default", "default"),
        ("selected_box", "black", "light gray"),
        ("confirm_button", "yellow", "dark blue"),
        ("abort_button", "light red", "brown"),
        ("progress_low", "default", "yellow"),
        ("progress_hight", "default", "dark green"),
        ("helper_key", "bold", "default"),
        ("helper_text_brown", "black", "brown"),
        ("helper_text_red", "black", "dark red"),
        ("helper_text_green", "black", "dark green"),
        ("helper_text_light", "white", "dark blue"),
    )

    def __init__(self, body, header=Text(("header", ""), "center"), footer=None):
        self.keybind = {}

        self.root = Frame(body, header, footer)
        self.loop = MainLoop(self.root, TUI.palette,
                             unhandled_input=self.unhandled_input)

        self.bind_global("f10", self.quit)
        self.handle_os_signals()

    def __call__(self):
        self.loop.run()

    def unhandled_input(self, key):
        if key in self.keybind:
            self.keybind[key]()
            return None

    def bind_global(self, key, callback):
        self.keybind[key] = callback

    def set_header_text(self, string):
        self.root.header.set_text(string)

    def clear_header(self):
        self.root.header.set_text("")

    def quit(self, *kargs):
        raise ExitMainLoop()

    def pause(self, *kargs):
        print("PAUSE")
        self.loop.stop()
        os.kill(os.getpid(), signal.SIGSTOP)
        self.loop.start()
        self.loop.draw_screen()

    def interrupt(self, *kargs):
        pass

    def handle_os_signals(self):

        if sys.platform != "win32":
            signal.signal(signal.SIGQUIT, self.quit)
            signal.signal(signal.SIGTSTP, self.pause)

        ###############################################################
        # TODO Windows:                                               #
        #                                                             #
        # sys.platform == win32 Should test for                       #
        # signal.CTRL_BREAK_EVENT and signal.CTRL_C_EVENT and hook to #
        # appropriate callback                                        #
        ###############################################################

        signal.signal(signal.SIGINT, self.interrupt)
