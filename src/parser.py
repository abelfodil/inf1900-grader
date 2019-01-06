
from optparse import OptionParser

from git import Repo
from os import path
from sys import argv

# Email a jerome
DEFAULT_RECEIVER = "olivier.dion@polymtl.ca"

def default_sender():

    repo = Repo(path.dirname(path.realpath(argv[0])))

    # Try to fetch from git configuration
    try:
        return repo.config_reader().get_value("user", "email")
    except:
        return ""


class Parser:

    def __init__(self):

        usage = "usage: %prog [options]"

        parser = OptionParser(usage=usage)

        # File to send option
        parser.add_option("-g", "--grading",
                          action="store", dest="csv_file",
                          type="string", default="grading_dir/grades.csv",
                          metavar="FILE", help="Send FILE by email")

        parser.add_option("-f", "--from",
                          action="store", dest="sender",
                          type="string", default=default_sender(),
                          metavar="EMAIL", help="EMAIL of the sender")

        parser.add_option("-t", "--to",
                          action="store", dest="receiver",
                          type="string", default=DEFAULT_RECEIVER,
                          metavar="EMAIL", help="EMAIL of the receiver")

        self.vargs = parser.parse_args()

    def get_options(self):
        return self.vargs[0]

    def get_args(self):
        return self.args[1]
