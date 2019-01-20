from os.path import isdir, isfile
from time import strptime

from validate_email import validate_email

time_format = "%Y-%m-%d %H:%M"


class InvalidInput(Exception):
    pass


def validate_email_address(email: str):
    if not validate_email(email):
        raise InvalidInput(f"Invalid email format: {email}")


def ensure_grading_directory_exists(directory_path: str):
    if not isdir(directory_path):
        raise InvalidInput(f"The grading directory \"{directory_path}\" does not exist. "
                           f"Please clone students repos first.")


def ensure_grading_directory_available(directory_path: str):
    if isdir(directory_path):
        raise InvalidInput(f"The grading directory \"{directory_path}\" already exists. "
                           f"Please delete it or resume grading.")


def ensure_not_empty(field, field_name: str):
    if not field:
        raise InvalidInput(f"Please enter a value for field \"{field_name}\"")


def validate_datetime(datetime: str):
    try:
        strptime(datetime, time_format)
    except ValueError:
        raise InvalidInput(f"Incorrect datetime format. "
                           f"Please use the following format: {time_format}")


def validate_grades_path(grades_path: str):
    if not isfile(grades_path):
        raise InvalidInput(f"The grades file \"{grades_path}\" does not exist.")
