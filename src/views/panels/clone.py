#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from urwid import LineBox, RadioButton

from src.models.clone import TeamType, clone
from src.models.state import state
from src.views.base.buffer import EditBuffer, IntEditBuffer
from src.views.base.form import Form
from src.views.base.signal import Signal
from src.views.panels.abstract import AbstractPanel


@Signal("on_quit")
class ClonePanel(AbstractPanel):

    def __init__(self):
        grading_directory = LineBox(EditBuffer(("header", "Grading directory\n\n"), state.grading_directory))
        group_number = LineBox(IntEditBuffer(("header", "Group number\n\n"), state.group_number))
        team_type_group = []
        type1 = RadioButton(team_type_group, TeamType.DUOS.name.capitalize())
        type2 = RadioButton(team_type_group, TeamType.QUARTET.name.capitalize())

        form = Form(clone,
                    grading_directory=grading_directory,
                    group_number=group_number,
                    team_type=team_type_group)

        super().__init__(grading_directory, form)
        self.tree.split_vertically(group_number)
        self.tree.split_vertically(type1)
        self.tree.split_vertically(type2)
        self.tree.split_vertically(self.buttons_column)
