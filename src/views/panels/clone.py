from urwid import Columns, LineBox, Filler

from src.models.clone          import TeamType, clone
from src.models.state          import state
from src.views.base.buffer     import EditBuffer, IntEditBuffer, RadioBuffer
from src.views.base.form       import Form
from src.views.base.grid       import Grid
from src.views.base.signal     import Signal
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

        super().__init__(form)

        grid = Grid([
            [grading_directory],
            [group_number, team_type.wrap],
            self.buttons
        ])

        grid.bind([
            ("up", lambda:grid.focus_vertical(-1)),
            ("down", lambda:grid.focus_vertical(1)),
            ("tab", grid.focus_next),
            ("shift tab", grid.focus_prev)
        ])

        grid.set_aliases([
            ("ctrl f", "left"),
            ("ctrl b", "right"),
            ("ctrl p", "up"),
            ("ctrl n", "down")
        ])

        grid.set_policy("vertical")


        self.root = Filler(grid, valign="top")
