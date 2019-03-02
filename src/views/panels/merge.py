from urwid import Edit, LineBox

from src.models.merge import merge
from src.models.state import state
from src.views.widgets.form import Form


class MergePanel(Form):

    def __init__(self):
        grading_directory = LineBox(Edit(("header", "Grading directory\n\n"), state.grading_directory))
        assignment_sname = LineBox(Edit(("header", "Assignment short name\n\n"), state.assignment_sname))

        grid_elements = [
            {"grading_directory": grading_directory, "assignment_sname": assignment_sname},
        ]

        super().__init__("Merge", grid_elements, merge)
