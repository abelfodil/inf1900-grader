from os import path
from sys import argv

from git import Repo

script_root_directory = path.dirname(path.realpath(argv[0]))


def get_grader_name():
    return Repo(script_root_directory).config_reader().get_value("user", "name")


def get_grader_email():
    return Repo(script_root_directory).config_reader().get_value("user", "email")


def get_assignment_subdirectories():
    subdirectories = input("What are the subdirectories to correct separated by space (ex: tp/tp6/pb1 tp/tp6/pb2)? ")
    return subdirectories.strip().split(" ")
