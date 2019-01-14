from urwid import Edit, IntEdit, LineBox

from src.models.grade import AssignmentType, grade
from src.models.state import state
from src.views.base.form import Form
from src.views.base.radio import RadioGroup
from src.views.base.signal import Signal, SignalType
from src.views.panels.abstract import AbstractPanel


@Signal(SignalType.QUIT)
class GradePanel(AbstractPanel):

    def __init__(self):
        grading_directory = LineBox(
            Edit(("header", "Grading directory\n\n"), state.grading_directory))
        subdirectories = LineBox(Edit(("header", "Subdirectories\n\n"), state.subdirectories))

        grader_name = LineBox(Edit(("header", "Grader's name\n\n"), state.grader_name))
        group_number = LineBox(IntEdit(("header", "Group number\n\n"), state.group_number))

        assignment_type = RadioGroup(AssignmentType, state.assignment_type)
        deadline = LineBox(Edit(("header", "Deadline\n\n"), state.deadline))

        assignment_sname = LineBox(
            Edit(("header", "Assignment short name\n\n"), state.assignment_sname))
        assignment_lname = LineBox(
            Edit(("header", "Assignment long name\n\n"), state.assignment_lname))

        grid_elements = [
            [grading_directory, subdirectories],
            [grader_name, group_number],
            [assignment_type, deadline],
            [assignment_sname, assignment_lname],
        ]

        form = Form(grade,
                    grading_directory=grading_directory,
                    subdirectories=subdirectories,
                    grader_name=grader_name,
                    group_number=group_number,
                    assignment_type=assignment_type,
                    deadline=deadline,
                    assignment_sname=assignment_sname,
                    assignment_lname=assignment_lname)

        super().__init__(grid_elements, form)
