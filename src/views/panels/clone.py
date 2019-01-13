from urwid import LineBox

from src.models.clone import TeamType, clone
from src.models.state import state
from src.views.base.buffer import EditBuffer, IntEditBuffer, RadioBuffer
from src.views.base.form import Form
from src.views.base.signal import Signal
from src.views.panels.abstract import AbstractPanel


@Signal("on_quit")
class ClonePanel(AbstractPanel):

    def __init__(self):
        grading_directory = LineBox(EditBuffer(("header", "Grading directory\n\n"),
                                               state.grading_directory))

        group_number = LineBox(IntEditBuffer(("header", "Group number\n\n"),
                                             state.group_number))

        team_type = RadioBuffer(TeamType, state.team_type)

        form = Form(clone,
                    grading_directory=grading_directory,
                    group_number=group_number,
                    team_type=team_type)

        grid_elements = [
            [grading_directory],
            [group_number, team_type.wrap],
        ]

        super().__init__(grid_elements, form)

