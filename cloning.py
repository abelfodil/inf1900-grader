from json import dump, load
from os import mkdir, path, getcwd
from urllib import request
from bs4 import BeautifulSoup
from git import Repo
from tabCompleter import tabCompleter
import readline

team_size_to_type = {
    2: "duos",
    4: "quatuors"
}

student_list_file = "students.json"


def get_student_list_path(grading_directory: str):
    return f"{grading_directory}/{student_list_file}"


def write_student_list(grading_directory: str, student_list: list):
    with open(get_student_list_path(grading_directory), 'w') as f:
        dump(student_list, f)


def read_student_list(grading_directory: str):
    student_list_path = get_student_list_path(grading_directory)
    if path.isfile(student_list_path):
        with open(student_list_path, 'r') as f:
            return load(f)
    else:
        return []


def clone_repos(grading_dir: str, student_list: list):
    unique_team_list = sorted(set([student['team'] for student in student_list]))
    for team in unique_team_list:
        team_repo_url = f"https://githost.gi.polymtl.ca/git/inf1900-{team}"
        output_dir = f"{grading_dir}/{team}"

        print(f"Cloning team {team}'s repository...")
        Repo.clone_from(team_repo_url, output_dir)


def fetch_student_list(team_type: str, group: str):
    group_url = f"http://www.groupes.polymtl.ca/inf1900/equipes/{team_type}Section{group}.php"
    html = BeautifulSoup(request.urlopen(group_url).read().decode("utf8"), features="html5lib")

    html_student_list = html.find_all("table")[-1].find_all("tr")[1:-1]
    student_list = []
    for html_student in html_student_list:
        html_student = html_student.find_all("td")

        student_list.append({
            "last_name": html_student[0].text.strip(),
            "first_name": html_student[1].text.strip(),
            "team": html_student[2].text.strip(),
        })

    return student_list

def get_dir_with_completion(prompt):
    t = tabCompleter()
    readline.set_completer_delims('\t')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(t.pathCompleter)
    user_input = input(prompt)
    return user_input

def get_grading_directory():
    pwd = getcwd()

    grading_directory = get_dir_with_completion("What is your grading directory? (Default : {}) ".format(pwd))

    if grading_directory == "":
        grading_directory = pwd

    return grading_directory

def clone():
    team_size = int(input("Are you correcting teams of two (2) or four (4) members? "))

    team_type = team_size_to_type[team_size]
    group = str(int(input("What is your group (ex: 1)? ")))
    grading_directory = get_grading_directory()

    if path.exists(grading_directory):
        print(f"{grading_directory} already exists. Please delete it or resume grading.")
    else:
        mkdir(grading_directory)
        student_list = fetch_student_list(team_type, group)
        write_student_list(grading_directory, student_list)
        clone_repos(grading_directory, student_list)

    return grading_directory, group
