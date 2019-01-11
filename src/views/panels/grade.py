#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from urwid import LineBox, Columns

from src.models import grade
from src.models.state import state
from src.views.base.buffer import Buffer
from src.views.base.form import Form
from src.views.base.signal import Signal
from src.views.panels.abstract import AbstractPanel


@Signal("on_quit")
class GradePanel(AbstractPanel):

    def __init__(self):
        grading_directory = LineBox(Buffer(("header", "Grading directory\n\n"), state.grading_directory))
        subdirectories = LineBox(Buffer(("header", "Subdirectories\n\n"), str(state.subdirectories)))
        directory_column = Columns([grading_directory, subdirectories])

        grader_name = LineBox(Buffer(("header", "Grader's name\n\n"), state.grader_name))
        group_number = LineBox(Buffer(("header", "Group number\n\n"), str(state.group_number)))
        grader_column = Columns([grader_name, group_number])

        assignment_type = LineBox(Buffer(("header", "Assignment type\n\n"), str(state.assignment_type)))
        deadline = LineBox(Buffer(("header", "Deadline\n\n"), state.deadline))
        assignment_column = Columns([assignment_type, deadline])

        assignment_sname = LineBox(Buffer(("header", "Assignment short name\n\n"), state.assignment_sname))
        assignment_lname = LineBox(Buffer(("header", "Assignment long name\n\n"), state.assignment_lname))
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
