from csv import writer
from datetime import datetime

import numpy as np

from src.models.clone import read_grading_info
from src.models.grade import generate_grading_file_name, get_teams_list
from src.models.validate import ensure_grading_directory_exists, ensure_not_empty, time_format


def extract_grade(team: str, grading_directory: str, assignment_sname: str):
    repo_path = f"{grading_directory}/{team}"
    grade_file_path = f"{repo_path}/{generate_grading_file_name(assignment_sname)}"

    with open(grade_file_path, 'r') as f:
        grading_file_content = f.read()
    grade_line = [line for line in grading_file_content.split('\n') if "Total: " in line][0]

    return float(grade_line.replace("Total:", "").replace("/20", "").strip())


def write_grades_file(grading_directory: str, grades_map: dict, assignment_sname: str):
    info = read_grading_info(grading_directory)
    group_number = info["group_number"]

    grades_path = f"{grading_directory}/notes-inf1900-sect0{group_number}-{assignment_sname}.csv"
    with open(grades_path, 'w', newline='', encoding="utf-8") as csvfile:
        csv_writer = writer(csvfile, delimiter=';')

        csv_writer.writerow(["Cours:", "INF1900"])
        csv_writer.writerow(["Correcteur:", info["grader_name"]])
        csv_writer.writerow(["Section:", group_number])
        csv_writer.writerow(["Date:", datetime.now().strftime(time_format)])
        csv_writer.writerow(["Travail:", assignment_sname])

        grades = np.array(list(grades_map.values()), dtype="float32")
        csv_writer.writerow([])
        csv_writer.writerow(["Moyenne:", np.mean(grades)])
        csv_writer.writerow(["Écart-type:", np.std(grades)])

        csv_writer.writerow([])
        csv_writer.writerow(["Nom", "Prénom", "Équipe", "Note"])

        for student_info in info["students"]:
            student_info["grade"] = str(grades_map[student_info["team"]]).replace(".", ",")
            csv_writer.writerow(student_info.values())


def assemble(grading_directory: str, assignment_sname: str):
    ensure_grading_directory_exists(grading_directory)
    ensure_not_empty(assignment_sname, "Assignment short name")

    teams = get_teams_list(grading_directory)
    grades = {team: extract_grade(team, grading_directory, assignment_sname) for team in teams}
    write_grades_file(grading_directory, grades, assignment_sname)
