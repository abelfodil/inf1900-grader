#!/usr/bin/env python3

from asking import SharedInformation
from cloning import clone
from grading import grade
from assembling import assemble

info = SharedInformation()

choices = [
    clone.__name__,
    grade.__name__,
    assemble.__name__
]

print("Welcome to INF1900 interactive grading tool")

while True:
    choice = input(f"What do you want to do? Please choose one of the following: {choices} ").strip()

    if choice in choices:
        globals()[choice](info)
    else:
        print("Incorrect parameter, please try again.")
