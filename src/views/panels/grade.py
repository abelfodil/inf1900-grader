#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from urwid import Columns, LineBox

from src.models.grade import AssignmentType, grade
from src.models.state import state
from src.views.base.buffer import EditBuffer, IntEditBuffer, RadioBuffer
from src.views.base.form import Form
from src.views.base.signal import Signal
from src.views.panels.abstract import AbstractPanel


@Signal("on_quit")
class GradePanel(AbstractPanel):

    def __init__(self):
        grading_directory = LineBox(EditBuffer(("header", "Grading directory\n\n"), state.grading_directory))
        subdirectories = LineBox(EditBuffer(("header", "Subdirectories\n\n"), state.subdirectories))
        directory_column = Columns([grading_directory, subdirectories])

        grader_name = LineBox(EditBuffer(("header", "Grader's name\n\n"), state.grader_name))
        group_number = LineBox(IntEditBuffer(("header", "Group number\n\n"), state.group_number))
        grader_column = Columns([grader_name, group_number])

        assignment_type = RadioBuffer(AssignmentType, state.assignment_type)
        deadline = LineBox(EditBuffer(("header", "Deadline\n\n"), state.deadline))
        assignment_column = Columns([assignment_type.wrap, deadline])

        assignment_sname = LineBox(EditBuffer(("header", "Assignment short name\n\n"), state.assignment_sname))
        assignment_lname = LineBox(EditBuffer(("header", "Assignment long name\n\n"), state.assignment_lname))
        assignment_name_column = Columns([assignment_sname, assignment_lname])

        form = Form(grade,
                    grading_directory=grading_directory,
                    subdirectories=subdirectories,
                    grader_name=grader_name,
                    group_number=group_number,
                    assignment_type=assignment_type,
                    deadline=deadline,
                    assignment_sname=assignment_sname,
                    assignment_lname=assignment_lname)

        super().__init__(directory_column, form)
        self.tree.split_vertically(grader_column)
        self.tree.split_vertically(assignment_column)
        self.tree.split_vertically(assignment_name_column)
        self.tree.split_vertically(self.buttons_column)
