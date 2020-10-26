from enum import Enum
from functools import partial
from multiprocessing import Pool
from os import listdir
from os.path import dirname, isdir, join, realpath
from subprocess import PIPE, STDOUT, run
from sys import argv

from git import Repo

from src.models.clone import read_grading_info
from src.models.validate import ensure_grading_directory_exists, ensure_not_empty, validate_datetime

script_root_directory = dirname(realpath(argv[0]))
bad_files_list = f"{script_root_directory}/samples/bad-files.gitignore"


class AssignmentType(Enum):
    CODE = f"{script_root_directory}/samples/grading_file_code.md"
    REPORT = f"{script_root_directory}/samples/grading_file_report.md"
    PROJECT = f"{script_root_directory}/samples/grading_file_project.md"


def get_teams_list(grading_directory: str):
    return [team for team in listdir(grading_directory) if
            isdir(join(grading_directory, team))]


def generate_partial_grading_file_content(grader_name: str, group_number: int,
                                          assignment_type: AssignmentType,
                                          assignment_long_name: str):
    with open(assignment_type.value, 'r') as f:
        raw_grading_file_content = f.read()

    partial_grading_file_content = raw_grading_file_content \
        .replace("__CORRECTEUR__", grader_name) \
        .replace("__SECTION__", str(group_number)) \
        .replace("__TRAVAIL_PRATIQUE__", assignment_long_name)

    return partial_grading_file_content


def bannerize(entry):
    return f"======================= {entry} ============================="

def md_coderize(entry):
    return f"```\n{entry}\n```"

def create_branch(repo_path: str, deadline: str, grading_name: str):
    repo = Repo(repo_path)
    deadline_commit = repo.git.rev_list("-n 1", f'--before="{deadline}"', "master")
    return repo.create_head(grading_name, deadline_commit)


def get_commit_info(repo_path: str):
    header = f"\n\n# Basé sur le commit suivant"
    commit_info = Repo(repo_path).git.log("-1")
    return f"{header}\n{md_coderize(commit_info)}"


def get_useless_files(repo_path: str):
    header = f"\n\n# Fichiers indésirables"
    useless_file_list = Repo(repo_path).git.ls_files("-i", f"--exclude-from={bad_files_list}")
    return f"{header}\n{md_coderize(useless_file_list)}"


def get_make_output(repo_path: str, subdirectories: list):
    header = f"\n\n# Sortie de make dans les sous-répertoires"

    make_output = ""
    for subdirectory in subdirectories:
        make_output += f"{bannerize(f'Sortie de make dans {subdirectory}')}"
        result = run(["make", "-C", f"{repo_path}/{subdirectory}"], stdout=PIPE, stderr=STDOUT)
        make_output += "\n" + result.stdout.decode('utf-8') + "\n"

    return f"{header}\n{md_coderize(make_output)}"


def generate_grading_name(assignment_short_name: str):
    return f"Correction_{assignment_short_name}"


def generate_grading_file_name(assignment_short_name: str):
    return f"{generate_grading_name(assignment_short_name)}.md"


def grade_team(team: str, grading_directory: str, subdirectories: list,
               partial_grading_text: str, deadline: str, assignment_sname: str):
    team_path = f"{grading_directory}/{team}"
    create_branch(team_path, deadline, generate_grading_name(assignment_sname)).checkout()

    grading_text = partial_grading_text.replace("__EQUIPE_NO__", team)
    grading_text += get_commit_info(team_path)
    grading_text += get_useless_files(team_path)
    grading_text += get_make_output(team_path, subdirectories)

    grade_file_path = f"{team_path}/{generate_grading_file_name(assignment_sname)}"
    with open(grade_file_path, 'w') as f:
        f.write(grading_text)


def grade(grading_directory: str, subdirectories: str,
          assignment_type: AssignmentType, deadline: str,
          assignment_sname: str, assignment_lname: str):
    ensure_grading_directory_exists(grading_directory)
    validate_datetime(deadline)
    subdirectories = subdirectories.strip()
    ensure_not_empty(subdirectories, "Subdirectories")
    ensure_not_empty(assignment_sname, "Assignment short name")
    ensure_not_empty(assignment_lname, "Assignment long name")

    info = read_grading_info(grading_directory)
    partial_grading_text = generate_partial_grading_file_content(info["grader_name"],
                                                                 info["group_number"],
                                                                 assignment_type, assignment_lname)

    teams = get_teams_list(grading_directory)
    with Pool(len(teams)) as p:
        partial_grade_team = partial(grade_team,
                                     grading_directory=grading_directory,
                                     partial_grading_text=partial_grading_text,
                                     deadline=deadline,
                                     assignment_sname=assignment_sname,
                                     subdirectories=subdirectories.split(" "))
        p.map(partial_grade_team, teams)
