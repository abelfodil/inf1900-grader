#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from src.views.controller import Controller
from src.views.signal     import Signal

from src.views.tree   import TreeWidget
from src.views.hydra  import HydraWidget
from src.views.buffer import Buffer, MiniBuffer
from src.views.button import Button

class WidgetException(Exception):

    def __init__(self, msg, *kargs, **kwargs):
        super().__init__(msg, *kargs, **kwargs)
