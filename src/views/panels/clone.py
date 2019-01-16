from urwid import Edit, IntEdit, LineBox

from src.models.clone import TeamType, clone
from src.models.state import state
from src.views.base.form import Form
from src.views.panels.abstract import AbstractPanel
from src.views.widgets.radio import RadioGroup


class ClonePanel(AbstractPanel):

    def __init__(self):
        grading_directory = LineBox(
            Edit(("header", "Grading directory\n\n"), state.grading_directory))
        group_number = LineBox(IntEdit(("header", "Group number\n\n"), state.group_number))
        team_type = RadioGroup("Team type", TeamType, state.team_type)

        grid_elements = [
            [grading_directory],
            [group_number, team_type],
        ]

        form = Form(clone,
                    grading_directory=grading_directory,
                    group_number=group_number,
                    team_type=team_type)

        super().__init__(grid_elements, form)
