from urwid import Filler, Text, WidgetWrap


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


class HydraWidget(WidgetWrap):
    def __init__(self, info):
        self.text = Text("", align="center")
        self.text._selectable = True  # glitch to make it work

        super().__init__(Filler(self.text, valign="middle"))

        self.keybind = {}
        self.heads = {}
        self.info = info

    def parse_hydra(self):
        markup = [("", f"{self.info}\n")]
        for letter, head in self.heads.items():
            markup.extend(head.urwid_text())

        self.text.set_text(markup)

    def keypress(self, size, key):
        if key in self.keybind:
            self.keybind[key]()
            return None
        elif key in self.heads:
            self.heads[key]()
            return None

        return key

    def add_heads(self, heads):
        for head in heads:
            self.heads[head[0]] = HydraHead(*head)

        self.parse_hydra()
