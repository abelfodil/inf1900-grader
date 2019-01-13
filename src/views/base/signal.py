class Signal:

    def __init__(self, *args, **kwargs):
        self.signals = args

    def __call__(self, *args):
        cls = args[0]

        cls.register(self.signals)

        return cls
