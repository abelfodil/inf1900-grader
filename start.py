#!/usr/bin/env python3

from cloning import clone
from grading import grade
from compiling import compile_grades


class Information:
    grading_directory = None
    assignment_name = None
    group = None


info = Information()

print("Welcome to INF1900 interactive grading tool")

while True:
    choice = input("What do you want to do? Please choose one of the following: "
                   "clone, grade, compile ").strip()

    if choice == "clone":
        clone(info)
    elif choice == "grade":
        grade(info)
    elif choice == "compile":
        compile_grades(info)
    else:
        print("Incorrect parameter, please try again.")
