from os import mkdir, path
from urllib import request
from bs4 import BeautifulSoup
from git import Repo

team_size_to_type = {
    2: "duos",
    4: "quatuors"
}


def clone_repos(grading_dir: str, student_list: list):
    if path.exists(grading_dir):
        print(f"{grading_dir} already exists. Please delete it or resume grading.")
        return

    mkdir(grading_dir)

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


def clone():
    team_size = int(input("Are you correcting teams of two (2) or four (4) members? "))
    team_type = team_size_to_type[team_size]
    group = str(int(input("What is your group (ex: 1)? ")))
    grading_directory = input("What is your grading directory? ")

    student_list = fetch_student_list(team_type, group)
    clone_repos(grading_directory, student_list)

    return grading_directory, group, student_list
