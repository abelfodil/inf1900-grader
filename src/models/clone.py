import json
from enum import Enum
from functools import partial
from multiprocessing import Pool
from os import mkdir
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from git import Repo

from src.models.validate import ensure_grading_directory_available, ensure_not_empty


class TeamType(Enum):
    DUOS = "duos"
    QUARTET = "quatuors"


def get_grading_info_path(grading_directory: str):
    return f"{grading_directory}/info.json"


def write_grading_info(grading_directory: str,
                       grader_name: str, group_number: int,
                       student_list: list):
    with open(get_grading_info_path(grading_directory), 'w') as f:
        json.dump({
            "grader_name": grader_name,
            "group_number": group_number,
            "students": student_list
        }, f)


def read_grading_info(grading_directory: str):
    with open(get_grading_info_path(grading_directory), 'r') as f:
        return json.load(f)


def clone_repo(team: str, grading_directory: str):
    team_repo_url = f"https://githost.gi.polymtl.ca/git/inf1900-{team}"
    output_directory = f"{grading_directory}/{team}"
    Repo.clone_from(team_repo_url, output_directory)


def fetch_student_list(group_number: int, team_type: TeamType):
    group_url = f"https://cours.polymtl.ca/inf1900/equipes/{team_type.value}Section{group_number}.php"

    raw_html = urlopen(Request(group_url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode("utf8")
    html = BeautifulSoup(raw_html, features="html5lib")

    html_student_list = html.find_all("table")[-1].find_all("tr")[1:-1]
    student_list = []
    for html_student in html_student_list:
        html_student = html_student.find_all("td")

        student_list.append({
            "last_name": html_student[0].text.strip(),
            "first_name": html_student[1].text.strip(),
            "team": html_student[2].text.strip(),
        })

    return sorted(student_list, key=lambda i: i["last_name"])


def clone(grading_directory: str, grader_name: str, group_number: int, team_type: TeamType):
    ensure_grading_directory_available(grading_directory)
    ensure_not_empty(group_number, "Group number")

    mkdir(grading_directory)
    student_list = fetch_student_list(group_number, team_type)
    write_grading_info(grading_directory, grader_name, group_number, student_list)

    unique_team_list = set([student['team'] for student in student_list])
    with Pool(len(unique_team_list)) as p:
        p.map(partial(clone_repo, grading_directory=grading_directory), unique_team_list)
