from urwid import Edit, LineBox, CheckBox

from src.models.assemble import assemble
from src.models.state import state
from src.views.widgets.form import Form


class AssemblePanel(Form):

    def __init__(self):
        grading_directory = LineBox(Edit(("header", "Grading directory\n\n"), state.grading_directory))
        assignment_sname = LineBox(Edit(("header", "Assignment short name\n\n"), state.assignment_sname))
        should_merge = LineBox(CheckBox(("header", "Commit and merge"), state.should_merge))

        grid_elements = [
            {"grading_directory": grading_directory, "assignment_sname": assignment_sname},
            {"should_merge": should_merge}
        ]

        super().__init__("Assemble", grid_elements, assemble)
