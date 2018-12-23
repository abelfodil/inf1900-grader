from os import listdir, path
from subprocess import run, PIPE, STDOUT
from git import Repo
from csv import writer, QUOTE_MINIMAL

from grading import generate_grading_file_name


def read_grade(grading_directory, team, assignment_name):
    repo_path = grading_directory + "/" + team
    grade_file_path = repo_path + "/" + generate_grading_file_name(assignment_name)

    with open(grade_file_path, 'r') as f:
        grading_file_content = f.read()

    grade = [line for line in grading_file_content.split('\n') if "Total: " in line][0]

    return float(grade.replace("Total: ", "").replace("/20", "").strip())


def write_grades_file(grades, student_list):
    with open('grades.csv', 'w', newline='') as csvfile:
        csv_writer = writer(csvfile, delimiter=',', quotechar='|', quoting=QUOTE_MINIMAL)

        csv_writer.writerow(["Nom", "Prénom", "Équipe", "Note"])

        for student_info in student_list:
            student_info["grade"] = grades[student_info["team"]]
            csv_writer.writerow(student_info.values())


def compile(grading_directory, assignment_name, student_list):
    if student_list is None:
        print("No student list available. Please clone directories first.")
        return

    if grading_directory is None:
        grading_directory = input("What is the grading directory? ")

    if assignment_name is None:
        assignment_name = input("What is the assignment name? ")

    teams = listdir(grading_directory)
    grades = {}
    for team in teams:
        grades[team] = read_grade(grading_directory, team, assignment_name)

    write_grades_file(grades, student_list)
