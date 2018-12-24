#!/usr/bin/env python3

from cloning import clone
from grading import grade
from assembling import assemble
from tabCompleter import tabCompleter

import readline

choices = [
    clone.__name__,
    grade.__name__,
    assemble.__name__
]

print("Welcome to INF1900 interactive grading tool")

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
    prompt = "What do you want to do? Please choose one of the following: {} ".format(choices)
    return get_choice_from_list(prompt, choices).strip()
  
while True:
    choice = get_main_choice()
    if choice in choices:
        globals()[choice]()
    else:
        print("Incorrect parameter, please try again.")
