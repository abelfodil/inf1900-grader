from functools import partial
from multiprocessing import Pool

from git import Repo

from src.models.grade import generate_grading_file_name, get_teams_list
from src.models.validate import ensure_grading_directory_exists, ensure_not_empty


def merge_team_grade(team: str, grading_directory: str, assignment_sname: str):
    repo = Repo(f"{grading_directory}/{team}")
    repo.index.add([generate_grading_file_name(assignment_sname)])
    repo.git.stash('--keep-index')
    repo.heads.master.checkout()
    repo.remotes.origin.pull()
    repo.index.commit(f"Correction du {assignment_sname}.")
    repo.remotes.origin.push()


def merge(grading_directory: str, assignment_sname: str):
    ensure_grading_directory_exists(grading_directory)
    ensure_not_empty(assignment_sname, "Assignment short name")

    teams = get_teams_list(grading_directory)
    with Pool(len(teams)) as p:
        partial_merge = partial(merge_team_grade,
                                grading_directory=grading_directory,
                                assignment_sname=assignment_sname)
        p.map(partial_merge, teams)
