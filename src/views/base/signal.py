from urwid import register_signal


class Signal:

    def __init__(self, *args):
        self.signals = args

    def __call__(self, *args):
        cls = args[0]
        register_signal(cls, self.signals)
        return cls
