from urwid import Edit, IntEdit, LineBox

from src.models.clone import TeamType, clone
from src.models.state import state
from src.views.widgets.form import Form
from src.views.widgets.radio import RadioGroup


class ClonePanel(Form):

    def __init__(self):
        grading_directory = LineBox(Edit(("header", "Grading directory\n\n"), state.grading_directory))
        grader_name = LineBox(Edit(("header", "Grader's name\n\n"), state.grader_name))
        group_number = LineBox(IntEdit(("header", "Group number\n\n"), state.group_number))
        team_type = RadioGroup("Team type", TeamType, state.team_type)
        username = LineBox(Edit(("header", "Username\n\n"), ""))
        password = LineBox(Edit(("header", "Password\n\n"), "", mask="*"))

        grid_elements = [
            {"grading_directory": grading_directory, "grader_name": grader_name},
            {"group_number": group_number, "team_type": team_type},
            {"username": username, "password": password},
        ]

        super().__init__("Clone", grid_elements, clone)
