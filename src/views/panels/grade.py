from urwid import Edit, IntEdit, LineBox

from src.models.grade import AssignmentType, grade
from src.models.state import state
from src.views.widgets.form import Form
from src.views.widgets.radio import RadioGroup


class GradePanel(Form):

    def __init__(self):
        grading_directory = LineBox(Edit(("header", "Grading directory\n\n"), state.grading_directory))
        subdirectories = LineBox(Edit(("header", "Subdirectories\n\n"), state.subdirectories))
        grader_name = LineBox(Edit(("header", "Grader's name\n\n"), state.grader_name))
        group_number = LineBox(IntEdit(("header", "Group number\n\n"), state.group_number))
        assignment_type = RadioGroup(("header", "Assignment type"), AssignmentType, state.assignment_type)
        deadline = LineBox(Edit(("header", "Deadline\n\n"), state.deadline))
        assignment_sname = LineBox(Edit(("header", "Assignment short name\n\n"), state.assignment_sname))
        assignment_lname = LineBox(Edit(("header", "Assignment long name\n\n"), state.assignment_lname))

        grid_elements = [
            {"grading_directory": grading_directory, "subdirectories": subdirectories},
            {"grader_name": grader_name, "group_number": group_number},
            {"assignment_type": assignment_type, "deadline": deadline},
            {"assignment_sname": assignment_sname, "assignment_lname": assignment_lname},
        ]

        super().__init__("Grade", grid_elements, grade)
