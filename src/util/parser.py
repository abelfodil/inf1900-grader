#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from optparse import OptionParser

class Parser:

    def __init__(self):

        usage = "usage: %prog [options]"

        parser = OptionParser(usage=usage)


        # Those options are useless, but it's good idea to keep them
        # as examples instead of reading the documentation again

        parser.add_option("-g", "--grading",
                          action="store", dest="csv_file",
                          type="string", default="grading_dir/grades.csv",
                          metavar="FILE", help="Send FILE by email")

        parser.add_option("-f", "--from",
                          action="store", dest="sender",
                          type="string", default="sender@polymtl.ca",
                          metavar="EMAIL", help="EMAIL of the sender")

        parser.add_option("-t", "--to",
                          action="store", dest="receiver",
                          type="string", default="receiver@polymtl.ca",
                          metavar="EMAIL", help="EMAIL of the receiver")

        self.vargs = parser.parse_args()

    def get_options(self):
        return self.vargs[0]

    def get_args(self):
        return self.vargs[1]
