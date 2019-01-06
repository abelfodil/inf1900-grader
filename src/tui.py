#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

import urwid

from src.hydra import Hydra
from src.mail import mail

class TUI:

    palette = [
        ("blue_head", "dark blue", ""),
        ("red_head", "dark red", "")
    ]

    modal_mode = 0
    edit_mode  = 1
    metaX_mode = 2

    echo_index        = 0
    hydra_index       = 1
    mini_buffer_index = 3

    def __init__(self):

        self.hydras      = {}                # Collection of hydras
        self.hydra       = None              # Current hydra
        self.mode        = TUI.modal_mode    # Current mode
        self.stack       = []                # Stack of hydra
        self.commands    = {}                # Global commands

        # Up
        self.echo_zone   = urwid.Text("")

        # Down
        self.mini_buff   = MiniBuffer(self)
        self.pile        = urwid.Pile([urwid.Divider("▁"),
                                       urwid.Text(""),
                                       urwid.Divider("─"),
                                       self.mini_buff], self.mini_buff)

        self.fill_up     = urwid.Filler(self.echo_zone, "top")
        self.fill_down   = urwid.Filler(self.pile, "bottom")

        pile             = urwid.Pile([self.fill_up, self.fill_down],
                                      self.fill_down)

        self.loop        = urwid.MainLoop(pile, TUI.palette,
                                          unhandled_input=self.key_pressed,
                                          handle_mouse=False)

    def select_mode(self, mode):

        self.mode = mode

        if mode == TUI.modal_mode:
            self.flush_mini_buffer()
        elif mode == TUI.edit_mode:
            self.activate_mini_buffer("> ")
        elif mode == TUI.metaX_mode:
            self.activate_mini_buffer("M-x: ")

    def echo(self, text):
        self.echo_zone.set_text(text)

    def key_pressed(self, key):

        if key == "meta x":
            self.select_mode(TUI.metaX_mode)

        elif key == "esc":
            self.select_mode(TUI.edit_mode)

        else:
            self.hydra.hydra.on_key(key)

    def activate_mini_buffer(self, prompt=""):
        self.mini_buff.set_caption(prompt)
        self.pile.focus_position = TUI.mini_buffer_index

    def flush_mini_buffer(self):
        self.saved_buff = self.mini_buff.get_edit_text()
        self.mini_buff.set_caption("")
        self.mini_buff.set_edit_text("")
        self.pile.focus_position = TUI.hydra_index

    def add_hydras(self, hydras):
        for hydra in hydras:
            self.hydras[hydra.name] = hydra

    def push_hydra(self, hydra):
        self.stack.append(hydra)

    def pop_hydra(self):
        self.set_hydra(self.stack.pop())

    def set_hydra(self, hydra):
        if hydra.name in self.hydras:

            try:
                self.hydra.hydra.post()
            except Exception as e:
                pass

            try:
                hydra.pre()
            except Exception as e:
                print(e)

            self.hydra = HydraBox(hydra)
            self.pile.contents[TUI.hydra_index] = (self.hydra.text, ('pack', None))
            self.flush_mini_buffer()

    def new_global_command(self, name, action):
        self.commands[name] = action

    # Launch event/draw loop
    def __call__(self):
        self.loop.run()

    # Force to quit
    @staticmethod
    def quit():
        raise urwid.ExitMainLoop()


class HydraBox:

    def __init__(self, hydra, *kargs, **kwargs):

        self.hydra = hydra

        markups = []

        markups.append(("", "{}\n".format(hydra.info)))

        for letter, head in self.hydra.heads.items():

            tmp_letter = None

            if head.exit_ == Hydra.t:
                tmp_letter = ("blue_head", head.letter)
            else:
                tmp_letter = ("red_head", head.letter)

            if head.hint != "":
                markups.append(("", "["))
                markups.append(tmp_letter)
                markups.append(("", "]: {}".format(head.hint)))
            else:
                markups.append(tmp_letter)

            markups.append(("", ", "))

        markups.pop()

        self.text = urwid.Text(markups, align="center")

class MiniBuffer(urwid.Edit):

    def __init__(self, tui, *kargs, **kwargs):
        super().__init__(*kwargs, **kwargs)
        self.tui = tui

    def keypress(self, size, key):

        if key == "esc":
            self.tui.toggle_mode()

        elif key == "enter":

            if self.tui.mode == TUI.metaX_mode:
                text = self.get_edit_text()

                if text in self.tui.global_commands:
                    self.tui.commands[text]()

        else:
            return super().keypress(size, key)



def foo():
    with open("foo", "w") as f:
        f.write("foo")


if __name__ == "__main__":

    tui = TUI()

    mail_hydra = mail(tui, None)

    menu_hydra = Hydra("menu", [], "My info.",
                       color=Hydra.amaranth)
    heads = [
        ('g', None),
        ('m', lambda:(tui.push_hydra(menu_hydra), tui.set_hydra(mail_hydra)), "mail", True),
        ('q', TUI.quit, "quit", Hydra.t)
    ]

    menu_hydra.add_heads(heads)

    hydras = [menu_hydra, mail_hydra]
    tui.add_hydras(hydras)

    tui.set_hydra(menu_hydra)

    tui()
