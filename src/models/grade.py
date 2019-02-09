from enum import Enum
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
    CODE = f"{script_root_directory}/samples/grading_file_code.txt"
    REPORT = f"{script_root_directory}/samples/grading_file_report.txt"


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


def create_branch(repo_path: str, deadline: str, grading_name: str):
    repo = Repo(repo_path)
    deadline_commit = repo.git.rev_list("-n 1", f'--before="{deadline}"', "master")
    return repo.create_head(grading_name, deadline_commit)


def get_commit_info(repo_path: str):
    header = f"\n\n{bannerize('Basé sur le commit suivant')}"
    commit_info = Repo(repo_path).git.log("-1")
    return f"{header}\n{commit_info}"


def get_useless_files(repo_path: str):
    header = f"\n\n{bannerize('Fichiers Indésirables')}"
    useless_file_list = Repo(repo_path).git.ls_files("-i", f"--exclude-from={bad_files_list}")
    return f"{header}\n{useless_file_list}"


def get_make_output(repo_path: str, subdirectories: list):
    header = f"\n\n{bannerize('Output de make pour les problemes')}"

    make_output = ""
    for subdirectory in subdirectories:
        make_output += f"{bannerize(f'output de make dans {subdirectory}')}"
        result = run(["make", "-C", f"{repo_path}/{subdirectory}"], stdout=PIPE, stderr=STDOUT)
        make_output += "\n" + result.stdout.decode('utf-8') + "\n"

    return f"{header}\n{make_output}"


def generate_grading_name(assignment_short_name: str):
    return f"Correction_{assignment_short_name}"


def generate_grading_file_name(assignment_short_name: str):
    return f"{generate_grading_name(assignment_short_name)}.txt"


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

    subdirectories_list = subdirectories.split(" ")
    teams = get_teams_list(grading_directory)
    for team in teams:
        repo_path = f"{grading_directory}/{team}"
        create_branch(repo_path, deadline, generate_grading_name(assignment_sname)).checkout()

        grading_text = partial_grading_text.replace("__TEAM_NUMBER__", team)
        grading_text += get_commit_info(repo_path)
        grading_text += get_useless_files(repo_path)
        grading_text += get_make_output(repo_path, subdirectories_list)

        grade_file_path = f"{repo_path}/{generate_grading_file_name(assignment_sname)}"
        with open(grade_file_path, 'w') as f:
            f.write(grading_text)
