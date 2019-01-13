from urwid import Edit, LineBox

from src.models.assemble import assemble
from src.models.state import state
from src.views.base.form import Form
from src.views.base.signal import Signal
from src.views.panels.abstract import AbstractPanel


@Signal("on_quit")
class AssemblePanel(AbstractPanel):

    def __init__(self):
        grading_directory = LineBox(
            Edit(("header", "Grading directory\n\n"), state.grading_directory))
        assignment_sname = LineBox(Edit(("header", "Assignment short name\n\n"), state.assignment_sname))

        grid_elements = [
            [grading_directory, assignment_sname]
        ]

        form = Form(assemble,
                    grading_directory=grading_directory,
                    assignment_sname=assignment_sname)

        super().__init__(grid_elements, form)
