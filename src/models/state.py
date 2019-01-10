from json import load, dump
from os.path import dirname, realpath, isfile
from sys import argv

from git import Repo

script_root_directory = dirname(realpath(argv[0]))
state_file_path = f"{script_root_directory}/state.json"


class ApplicationState:
    def __init__(self):
        loaded_state = self.__load_state()
        self.internal = loaded_state if loaded_state else self.__default_state()

    def __save_state(self):
        with open(state_file_path, 'w') as f:
            dump(self.internal, f)

    def override_state(self, **kwargs):
        self.internal = {**self.internal, **kwargs}
        self.__save_state()

    @staticmethod
    def __default_state():
        repo = Repo(script_root_directory)
        return {
            "grader_name" : repo.config_reader().get_value("user", "name"),
            "grader_email": repo.config_reader().get_value("user", "email"),
            # "receiver"    : "jerome.collin@polymtl.ca",
            "receiver"    : "test@test.com",  # TODO: remove this
            "subject"     : "[NO-REPLY] inf1900-grader",
            "message"     : "Correction d'un travail terminée.",
        }

    @staticmethod
    def __load_state():
        if not isfile(state_file_path):
            return {}

        with open(state_file_path, 'r') as f:
            return load(f.read())


state = ApplicationState()
