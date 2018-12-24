#!/usr/bin/env python3

from os import path
from cloning import clone
from grading import grade
from compiling import compile_grades
from json import dump, load
from tabCompleter import tabCompleter
import readline

student_list_file = "students.json"

print("Welcome to INF1900 interactive grading tool")

grading_directory = None
assignment_name = None
student_list = None
group = None

if path.isfile(student_list_file):
    with open('students.json', 'r') as f:
        student_list = load(f)

def get_choice_from_list(prompt, choices):
    t = tabCompleter()
    t.createListCompleter(choices)

    readline.set_completer_delims('\t')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(t.listCompleter)

    return input(prompt)

def get_main_choice():
    choices = ['clone', 'grade', 'compile']
    prompt = "What do you want to do? Please choose one of the following: {} ".format(choices)
    return get_choice_from_list(prompt, choices).strip()


while True:
    choice = get_main_choice()

    if choice == "clone":
        grading_directory, group, student_list = clone()
        with open(student_list_file, 'w') as f:
            dump(student_list, f)
    elif choice == "grade":
        grading_directory, group, assignment_name = grade(grading_directory, group)
    elif choice == "compile":
        compile_grades(grading_directory, assignment_name, student_list)
    else:
        print("Incorrect parameter, please try again.")
