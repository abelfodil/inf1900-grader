#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from urwid import Text


class HydraHead:
    def __init__(self, letter, letter_color, hint, func, params={}):
        self.letter = letter
        self.letter_color = letter_color
        self.hint = hint
        self.func = func
        self.params = params

    def urwid_text(self):
        return [("", "["), (self.letter_color, self.letter), ("", f"]: {self.hint} ")]

    def __call__(self):
        self.func(**self.params)


class HydraWidget(Text):
    def __init__(self, info, *kargs, **kwargs):
        super().__init__("", *kargs, **kwargs)

        self.keybind = {}
        self.heads = {}
        self.info = info

        # Glitch to make it work
        self._selectable = True

    def parse_hydra(self):
        markup = [("", f"{self.info}\n")]
        for letter, head in self.heads.items():
            markup.extend(head.urwid_text())

        self.set_text(markup)

    def keypress(self, size, key):
        if key in self.heads:
            self.heads[key]()
            return None

        return key

    def add_heads(self, heads):
        for head in heads:
            self.heads[head[0]] = HydraHead(*head)

        self.parse_hydra()
