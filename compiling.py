from csv import writer
from git import Repo
from cloning import read_student_list
from grading import generate_grading_file_name, get_teams_list


def read_grade(grading_directory: str, team: str, assignment_name: str):
    repo_path = f"{grading_directory}/{team}"
    grade_file_path = f"{repo_path}/{generate_grading_file_name(assignment_name)}"

    with open(grade_file_path, 'r') as f:
        grading_file_content = f.read()

    grade = [line for line in grading_file_content.split('\n') if "Total: " in line][0]

    return str(float(grade.replace("Total: ", "").replace("/20", "").strip())).replace(".", ",")


def write_grades_file(grading_directory: str, grades: dict):
    student_list = read_student_list(grading_directory)

    with open(f"{grading_directory}/grades.csv", 'w', newline='') as csvfile:
        csv_writer = writer(csvfile)

        csv_writer.writerow(["Nom", "Prénom", "Équipe", "Note"])

        for student_info in student_list:
            student_info["grade"] = grades[student_info["team"]]
            csv_writer.writerow(student_info.values())


def commit_and_merge(grading_directory: str, team: str, assignment_name: str):
    repo = Repo(f"{grading_directory}/{team}")
    repo.index.add([generate_grading_file_name(assignment_name)])
    repo.index.commit(f"Correction du {assignment_name}.")

    grading_branch = repo.active_branch
    master = repo.branches["master"]

    repo.git.pull('origin', master)
    repo.git.checkout("master")
    repo.git.merge(grading_branch)
    repo.git.push('origin', master)


def compile_grades(grading_directory: str, assignment_name: str):
    if grading_directory is None:
        grading_directory = input("What is the grading directory? ")

    if assignment_name is None:
        assignment_name = input("What is the assignment name? ")

    teams = get_teams_list(grading_directory)
    grades = {}
    for team in teams:
        print(f"Sending grades to team {team}...")

        commit_and_merge(grading_directory, team, assignment_name)
        grades[team] = read_grade(grading_directory, team, assignment_name)

    write_grades_file(grading_directory, grades)
