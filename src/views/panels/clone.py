#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from urwid import Columns, LineBox

from src.models.clone import TeamType, clone
from src.models.state import state
from src.views.base.buffer import EditBuffer, IntEditBuffer, RadioBuffer
from src.views.base.form import Form
from src.views.base.signal import Signal
from src.views.panels.abstract import AbstractPanel


@Signal("on_quit")
class ClonePanel(AbstractPanel):

    def __init__(self):
        grading_directory = LineBox(EditBuffer(("header", "Grading directory\n\n"), state.grading_directory))

        group_number = LineBox(IntEditBuffer(("header", "Group number\n\n"), state.group_number))
        team_type = RadioBuffer([
            (TeamType.DUOS.name.capitalize(), TeamType.DUOS),
            (TeamType.QUARTET.name.capitalize(), TeamType.QUARTET)
        ])

        group_detail_column = Columns([group_number, team_type.wrap])

        form = Form(clone,
                    grading_directory=grading_directory,
                    group_number=group_number,
                    team_type=team_type)

        super().__init__(grading_directory, form)
        self.tree.split_vertically(group_detail_column)
        self.tree.split_vertically(self.buttons_column)
