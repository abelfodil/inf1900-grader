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


def md_coderize(entry):
    return f"```\n{entry}\n```"


def checkout_commit_before_deadline(repo_path: str, deadline: str):
    repo = Repo(repo_path)
    deadline_commit = repo.git.rev_list("-n 1", f'--before="{deadline}"', "master")
    repo.git.checkout(deadline_commit)


def get_commit_info(repo_path: str):
    header = f"\n\n# Basé sur le commit suivant"
    commit_info = Repo(repo_path).git.log("-1")
    return f"{header}\n{md_coderize(commit_info)}"


def get_useless_files(repo_path: str, subdirectories: list):
    return Repo(repo_path).git.ls_files("-ico", f"--exclude-from={bad_files_list}", *subdirectories)


def get_relevant_useless_files(repo_path: str, subdirectories: list):
    header = f"\n\n# Fichiers indésirables pertinents"
    useless_file_list = get_useless_files(repo_path, subdirectories)
    formatted_useless_file_list = md_coderize(useless_file_list) if useless_file_list else 'Aucun'
    return f"{header}\n{formatted_useless_file_list}"


def get_all_useless_files(repo_path: str):
    header = f"\n\n# Tous les fichiers indésirables"
    useless_file_list = get_useless_files(repo_path, [])
    formatted_useless_file_list = md_coderize(useless_file_list) if useless_file_list else 'Aucun'
    return f"{header}\n{formatted_useless_file_list}"


def make(repo_path: str, subdirectory: str):
    run(["make", "-C", f"{repo_path}/{subdirectory}", "clean"], stdout=PIPE, stderr=STDOUT)
    return run(["make", "-C", f"{repo_path}/{subdirectory}"], stdout=PIPE, stderr=STDOUT).stdout.decode('utf-8')


def formatted_make(repo_path: str, subdirectory: str):
    header = f'\n## Sortie de `make` dans `{subdirectory}`'
    result = make(repo_path, subdirectory)
    return f"{header}\n{md_coderize(result)}\n"


def get_formatted_make_outputs(repo_path: str, subdirectories: list):
    header = f"\n\n# Sorties de `make` dans les sous-répertoires"

    formatted_outputs = [formatted_make(repo_path, subdirectory) for subdirectory in subdirectories]
    formatted_outputs = ''.join(formatted_outputs)

    return f"{header}\n{formatted_outputs}"


def generate_grading_file_name(assignment_short_name: str):
    return f"Correction_{assignment_short_name}.md"


def grade_team(team: str, grading_directory: str, subdirectories: list,
               partial_grading_text: str, deadline: str, assignment_sname: str):
    team_path = f"{grading_directory}/{team}"

    checkout_commit_before_deadline(team_path, deadline)

    grading_text = partial_grading_text.replace("__EQUIPE_NO__", team)
    grading_text += get_commit_info(team_path)
    grading_text += get_relevant_useless_files(team_path, subdirectories)
    grading_text += get_all_useless_files(team_path)
    grading_text += get_formatted_make_outputs(team_path, subdirectories)

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
