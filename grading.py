from os import listdir, path
from subprocess import run, PIPE, STDOUT
from git import Repo
from csv import writer, QUOTE_MINIMAL

assignment_type_to_grading_file = {
    "code": "grading_sample_file.txt",
    "report": "grading_sample_file_tp7.txt"
}


def generate_partial_grading_file(assignment_name, group, grader_name, assignment_type):
    with open(assignment_type_to_grading_file[assignment_type], 'r') as f:
        raw_grading_file_content = f.read()

    partial_grading_file_content = raw_grading_file_content \
        .replace("__TRAVAIL_PRATIQUE__", assignment_name) \
        .replace("__SECTION__", group) \
        .replace("__CORRECTEUR__", grader_name)

    return partial_grading_file_content


def create_branch(repo_path, deadline, grading_name):
    repo = Repo(repo_path)
    deadline_commit = repo.git.rev_list("-n 1", '--before="' + deadline + '"', "master")
    return repo.create_head(grading_name, deadline_commit)


def get_commit_info(repo_path):
    header = "======================= Basé sur le commit suivant ============================="
    commit_info = Repo(repo_path).git.log("-1")

    return header + "\n" + commit_info


def get_useless_files(repo_path):
    header = "====================== Fichiers Indésirables ==================================="

    root_directory = path.dirname(path.realpath(__file__))
    bad_files_list = root_directory + "/bad-files.gitignore"
    useless_file_list = Repo(repo_path).git.ls_files("-i", "--exclude-from=" + bad_files_list)

    return header + "\n" + useless_file_list


def get_make_output(repo_path, subdirectories):
    header = "====================== Output de make pour les problemes ======================="

    make_output = ""

    for subdirectory in subdirectories:
        make_output += "============== output make dans " + subdirectory + " ============================"
        result = run(["make", "-C", repo_path + "/" + subdirectory], stdout=PIPE, stderr=STDOUT)
        make_output += "\n" + result.stdout.decode('utf-8') + "\n"

    return header + "\n" + make_output


def generate_grading_name(assignment_name):
    return "Correction_" + assignment_name


def generate_grading_file_name(assignment_name):
    return generate_grading_name(assignment_name) + ".txt"


def grade_all(grading_directory, subdirectories, deadline, assignment_name, partial_grading_text):
    subdirectories_list = subdirectories.strip().split(" ")

    teams = listdir(grading_directory)
    for team in teams:
        repo_path = grading_directory + "/" + team
        create_branch(repo_path, deadline, generate_grading_name(assignment_name)).checkout()

        grading_text = partial_grading_text.replace("__TEAM_NUMBER__", team)
        grading_text += "\n\n" + get_commit_info(repo_path)
        grading_text += "\n\n" + get_useless_files(repo_path)
        grading_text += "\n\n" + get_make_output(repo_path, subdirectories_list)

        grade_file_path = repo_path + "/" + generate_grading_file_name(assignment_name)
        with open(grade_file_path, 'w') as f:
            f.write(grading_text)


def grade(grading_directory):
    grader_name = input("What is your name? ")
    assignment_name = input("What is the assignment name? ")
    assignment_type = input("Is it a 'code' assignment or a 'report'? ")
    group = input("What is your group? ")

    partial_grading_text = generate_partial_grading_file(assignment_name, group, grader_name, assignment_type)

    if grading_directory is None:
        grading_directory = input("What is the grading directory? ")

    deadline = input("What is the assignment deadline (yyyy-mm-dd hh:mm)? ")
    subdirectories = input("What are the subdirectories to correct separated by space (ex: tp/tp6/pb1 tp/tp6/pb2)? ")

    grade_all(grading_directory, subdirectories, deadline, assignment_name, partial_grading_text)

    return grading_directory, assignment_name
