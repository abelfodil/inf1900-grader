#!/usr/bin/env python3

from os import path
from cloning import clone
from grading import grade
from compiling import compile_grades
from json import dump, load

student_list_file = "students.json"

print("Welcome to INF1900 interactive grading tool")

grading_directory = None
assignment_name = None
student_list = None
group = None

if path.isfile(student_list_file):
    with open('students.json', 'r') as f:
        student_list = load(f)

while True:
    choice = input("What do you want to do? Please choose one of the following: "
                   "clone, grade, compile, quit ").strip()

    if choice == "clone":
        grading_directory, group, student_list = clone()
        with open(student_list_file, 'w') as f:
            dump(student_list, f)
    elif choice == "grade":
        grading_directory, group, assignment_name = grade(grading_directory, group)
    elif choice == "compile":
        compile_grades(grading_directory, assignment_name, student_list)
    elif choice == "quit":
        exit(0)
    else:
        print("Incorrect parameter, please try again.")
