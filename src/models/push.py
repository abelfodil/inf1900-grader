from functools import partial
from multiprocessing import Pool
from shutil import make_archive
from datetime import datetime


from git import Repo

from src.models.grade import generate_grading_file_name, get_teams_list
from src.models.validate import ensure_grading_directory_exists, ensure_not_empty


def backup_repo(repo_path: str):
    now = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    output_path = f"{repo_path}.{now}"
    make_archive(output_path, 'zip', repo_path)


def push_team_grade_file(team: str, grading_directory: str, assignment_sname: str):
    repo_path = f"{grading_directory}/{team}"

    backup_repo(repo_path)

    repo = Repo(repo_path)
    repo.index.add([generate_grading_file_name(assignment_sname)])
    repo.git.clean('-ffxd')
    repo.git.restore('.')
    repo.heads.master.checkout()
    repo.index.commit(f"Correction du {assignment_sname}")
    repo.remotes.origin.pull(rebase=True)
    repo.remotes.origin.push()


def push(grading_directory: str, assignment_sname: str):
    ensure_grading_directory_exists(grading_directory)
    ensure_not_empty(assignment_sname, "Assignment short name")

    teams = get_teams_list(grading_directory)
    with Pool(len(teams)) as p:
        partial_push = partial(push_team_grade_file,
                               grading_directory=grading_directory,
                               assignment_sname=assignment_sname)
        p.map(partial_push, teams)
