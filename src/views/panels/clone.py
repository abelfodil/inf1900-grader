#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from urwid import LineBox

from src.models import clone
from src.models.state import state
from src.views.base.buffer import Buffer
from src.views.base.form import Form
from src.views.base.signal import Signal
from src.views.panels.abstract import AbstractPanel


@Signal("on_quit")
class ClonePanel(AbstractPanel):

    def __init__(self):
        grading_directory = LineBox(Buffer(("header", "Grading directory\n\n"), state.grading_directory))
        group_number  = LineBox(Buffer(("header", "Group number\n\n"), str(state.group_number)))
        team_type = None

        form = Form(clone,
                    grading_directory=grading_directory,
                    group_number=group_number,
                    team_type=team_type)

        super().__init__(grading_directory, form)
        self.tree.split_vertically(group_number)
        # self.tree.split_vertically(team_type)
        self.tree.split_vertically(self.buttons_column)
