import re
from csv import writer
from datetime import datetime
from io import StringIO
from statistics import mean, stdev

from src.models.clone import read_grading_info
from src.models.grade import generate_grading_file_name, get_teams_list
from src.models.validate import InvalidInput, ensure_grading_directory_exists, ensure_not_empty, time_format

TOTAL_KEYWORD = "Total"
GRADE_REGEX = fr"{TOTAL_KEYWORD}\D*(\d+(?:\.|,)\d+|\d+)\s*/"


def extract_grade(team: str, grading_directory: str, assignment_sname: str):
    repo_path = f"{grading_directory}/{team}"
    grade_file_path = f"{repo_path}/{generate_grading_file_name(assignment_sname)}"

    with open(grade_file_path, 'r') as f:
        grading_file_content = f.read()

    try:
        raw_grade = re.search(GRADE_REGEX, grading_file_content).group(1)
        grade = float(raw_grade.replace(',', '.'))
        return grade
    except:
        raise InvalidInput(f"Missing or invalid grade for team {team}.")


def add_grade_to_student_info(student_info: list, grades_map: dict):
    return {**student_info,
            'grade': grades_map[student_info["team"]]
            }


def write_grades_file(grading_directory: str, grades_map: dict, assignment_sname: str):
    info = read_grading_info(grading_directory)
    group_number = info["group_number"]

    csv_output = StringIO()
    csv_writer = writer(csv_output, delimiter=';')
    csv_writer.writerows([
        ["Cours:", "INF1900"],
        ["Correcteur:", info["grader_name"]],
        ["Section:", group_number],
        ["Date:", datetime.now().strftime(time_format)],
        ["Travail:", assignment_sname],
        [],
        ["Moyenne:", mean(grades_map.values())],
        ["Écart-type:", stdev(grades_map.values())],
        [],
        ["Nom", "Prénom", "Équipe", "Note"],
        *[list(add_grade_to_student_info(student_info, grades_map).values()) for student_info in info["students"]]
    ])

    # Hack: replace dot decimals with comma decimals
    csv_output = csv_output.getvalue().replace(".", ",")

    grades_path = f"{grading_directory}/notes-inf1900-sect0{group_number}-{assignment_sname}.csv"
    with open(grades_path, 'w', newline='', encoding="utf-8") as csvfile:
        csvfile.write(csv_output)


def assemble(grading_directory: str, assignment_sname: str):
    ensure_grading_directory_exists(grading_directory)
    ensure_not_empty(assignment_sname, "Assignment short name")

    teams = get_teams_list(grading_directory)
    grades = {team: extract_grade(team, grading_directory, assignment_sname) for team in teams}
    write_grades_file(grading_directory, grades, assignment_sname)
