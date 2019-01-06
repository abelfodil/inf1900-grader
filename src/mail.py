# Author: Olivier Dion - 2019

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

from src.hydra import Hydra

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


def confirm_mail(tui, options):

    text = """
    Send file: {}
    TO:        {}
    FROM:      {}""".format(options.csv_file,
                            options.receiver,
                            options.sender)
    tui.echo(text)


def mail(tui, options):

    mail_heads = [
        ("y",
         lambda:Mail(options.csv_file, options.sender, options.receiver).send(),
         "yes"),
        ("n", None, "no")
    ]

    mail_hydra = Hydra("mail", mail_heads, "Mail Menu",
                       on_kill=lambda:tui.pop_hydra(),
                       pre=lambda: confirm_mail(tui, options),
                       color=Hydra.teal)

    return mail_hydra
