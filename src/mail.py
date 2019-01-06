# Author: Olivier Dion - 2019

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base      import MIMEBase

from src.ask import get_grading_directory
from src.ask import get_grader_email

default_subject  = "[DO NOT REPLY] inf1900-grader"

# You can spam that one
default_receiver = "olivier-dion@hotmail.com"

class MailException(Exception):

    def __init__(self, msg):
        super().__init__(msg)

class MailAttachment:

    def __init__(self, type_, filename):

        self.filename = filename
        self.main_type, self.sub_type = type_.split("/")

    def to_MIME(self):

        with open(self.filename, "rb") as f:
            base = MIMEBase(self.main_type,
                            self.sub_type)
            base.set_payload(f.read())
            base.add_header("Content-Disposition",
                            "attachment",
                            filename=self.filename)

            return base

class Mail:

    def __init__(self, subject, sender, receiver, attachments=[]):

        msg = MIMEMultipart()

        msg["Subject"] = subject
        msg["From"]    = sender
        msg["To"]      = receiver

        self.filename_list  = []

        for attachment in attachments:

            self.filename_list.append(attachment.filename)
            msg.attach(attachment.to_MIME())

        self.msg = msg
        self.was_sent = False

    def send(self, smtp_addr="smtp.polymtl.ca", port=587):

        if self.was_sent:
            raise MailException("Mail was already sent!")

        smtp = smtplib.SMTP(smtp_addr, port)
        smtp.send_message(self.msg, self.msg["From"], self.msg["To"])
        smtp.quit()

        self.was_sent = True


def mail():

    receiver = default_receiver
    sender   = f"{get_grader_email()}"
    filename = f"{get_grading_directory(True)}/grades.csv"

    attachments = [MailAttachment("text/csv",
                                  filename)]

    mail = Mail(default_subject,
                sender,
                receiver,
                attachments)

    while 1:
        print("You're about to send the file {}".format(filename))
        print("FROM: {}".format(sender))
        print("TO:   {}".format(receiver))

        answer = input("Are you sure of this operation? [y/n] ").strip().lower()

        if answer[0] == 'y':
            mail.send()
            break

        elif answer[0]== 'n':
            break

        else:
            print("Invalid answer")
