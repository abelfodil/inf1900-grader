#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################


class WidgetException(Exception):

    def __init__(self, msg, *kargs, **kwargs):
        super().__init__(msg, *kargs, **kwargs)
