#!/usr/bin/env python3

from cloning import clone
from grading import grade
from compiling import compile_grades

print("Welcome to INF1900 interactive grading tool")

grading_directory = None
assignment_name = None
group = None

while True:
    choice = input("What do you want to do? Please choose one of the following: "
                   "clone, grade, compile ").strip()

    if choice == "clone":
        grading_directory, group = clone()
    elif choice == "grade":
        grading_directory, group, assignment_name = grade(grading_directory, group)
    elif choice == "compile":
        compile_grades(grading_directory, assignment_name)
    else:
        print("Incorrect parameter, please try again.")
