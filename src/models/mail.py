# Author: Olivier Dion - 2019

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from os.path import isfile

default_receiver = "jerome.collin@polymtl.ca"
default_subject = "[NO-REPLY] inf1900-grader"
default_message = "Correction d'un travail terminée."


class MailException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class MailAttachment:
    def __init__(self, type_, path, filename):
        self.path = path
        self.filename = filename
        self.main_type, self.sub_type = type_.split("/")

    def to_MIME(self):
        with open(self.path, "rb") as f:
            base = MIMEBase(self.main_type, self.sub_type)
            base.set_payload(f.read())
            base.add_header("Content-Disposition", "attachment", filename=self.filename)

            return base


class Mail:
    def __init__(self, sender, receiver, subject, message="", attachments=[]):

        msg = MIMEMultipart()

        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver

        msg.attach(MIMEText(message))

        for attachment in attachments:
            msg.attach(attachment.to_MIME())

        self.msg = msg
        self.sent = False

    def send(self, smtp_addr="smtp.polymtl.ca", port=587):

        if self.sent:
            raise MailException("Mail was already sent!")

        smtp = smtplib.SMTP(smtp_addr, port)
        smtp.send_message(self.msg, self.msg["From"], self.msg["To"])
        smtp.quit()

        self.sent = True


def mail(sender: str, recipient: str, subject: str, message: str, grades_path: str):
    attachments = [MailAttachment("text/csv", grades_path, grades_path.replace("/", "_"))]
    Mail(sender, recipient, subject, message, attachments).send()
