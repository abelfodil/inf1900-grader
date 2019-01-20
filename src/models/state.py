from os.path import dirname, realpath
from pickle import dump, load
from sys import argv
from time import localtime, strftime

from git import Repo

from src.models.clone import TeamType
from src.models.grade import AssignmentType
from src.models.validate import time_format
from src.util.singleton import Singleton

script_root_directory = dirname(realpath(argv[0]))
state_file_path = f"{script_root_directory}/user.bin"


class ApplicationState(metaclass=Singleton):
    def __init__(self):
        loaded_state = self.__load_state()
        self.__dict__ = loaded_state if loaded_state else self.__default_state()

    def __save_state(self):
        with open(state_file_path, 'wb') as f:
            dump(self.__dict__, f)

    def override_state(self, **kwargs):
        self.__dict__ = {**self.__dict__, **kwargs}
        self.__save_state()

    @staticmethod
    def __default_state():
        name = ""
        email = ""
        try:
            repo = Repo(script_root_directory)
            name = repo.config_reader().get_value("user", "name")
            email = repo.config_reader().get_value("user", "email")
        except:
            pass

        return {
            "grader_name"      : name,
            "sender_email"     : email,
            "recipient_email"  : "jerome.collin@polymtl.ca",
            "subject"          : "[inf1900-grader] TP#",
            "message"          : "Correction d'un travail terminée.",
            "deadline"         : strftime(time_format, localtime()),
            "assignment_sname" : "tp6",
            "assignment_lname" : "Capteurs et conversion analogique/numérique",
            "group_number"     : 1,
            "team_type"        : TeamType.DUOS,
            "grading_directory": "correction_tp6",
            "assignment_type"  : AssignmentType.CODE,
            "subdirectories"   : "tp/tp6/pb1 tp/tp6/pb2",
        }

    @staticmethod
    def __load_state():
        try:
            with open(state_file_path, 'rb') as f:
                return load(f)
        except:
            return {}


state = ApplicationState()
