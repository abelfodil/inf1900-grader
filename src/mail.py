# Author: Olivier Dion - 2019

# Mail client
import smtplib

# MIME types
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

# ANSI escape code Colors
NORMAL = "\033[0m"
BOLD   = "\033[1m"
RED    = "\033[38;2;255;0;0m"
GREEN  = "\033[38;2;0;255;0m"
YELLOW = "\033[38;2;255;255;0m"


# Maybe put this in a class so we can reeuse it in other modules?
def ok(msg):
    return (GREEN + msg + NORMAL)

def warning(msg):
    return (YELLOW + msg + NORMAL)

def error(msg):
    return (RED + msg + NORMAL)

def bold(msg):
    return (BOLD + msg + NORMAL)


class Mail:

    # file_ The CSV file to read from
    #
    # from_ Sender of email
    #
    # to_   Receiver of email
    def __init__(self, file_, from_, to_):

        msg = MIMEMultipart()

        msg["Subject"] = "[DO NOT REPLY] inf1900-grader"
        msg["From"]    = from_
        msg["To"]      = to_

        # Read file and create MIME type for csv type
        with open(file_, "rb") as f:
            csv = MIMEBase("text", "csv")
            csv.set_payload(f.read())
            csv.add_header("Content-Disposition", "attachment", filename=file_)
            msg.attach(csv)

        self.msg = msg

    # Connect to smtp.polymtl.ca and send email
    def send(self):
        smtp = smtplib.SMTP("smtp.polymtl.ca", port=587)
        smtp.send_message(self.msg, self.msg["From"], self.msg["To"])
        smtp.quit()

    # For debugging purpose
    def echo(self):
        print(self.msg.as_string())


def resolve_sender():

    print("I can't find a valid sender name.")
    print("Please set your email with git so I can use it.")


def mail(options, args):

    if options.sender == "":
        resolve_sender()
        print("Operation {}".format(warning("ABORTED")))
        exit(1)


    filename = options.csv_file
    sender   = options.sender
    receiver = options.receiver

    while 1:
        print("You're about to send the file {}".format(bold(filename)))
        print("FROM: {}".format(sender))
        print("TO:   {}".format(receiver))

        answer = input("Are you sure of this operation? [y/n] ")

        if answer[0].lower() == 'y':
            try:
                Mail(filename, sender, receiver).send()
                print("Operation {}".format(ok("TERMINATED")))
            except Exception as e:
                print(e)
                print("Operation {}".format(error("FAILED")))

            break

        elif answer[0].lower() == 'n':
            print("Operation {}".format(warning("ABORTED")))
            break

        else:
            print("Invalid answer")
