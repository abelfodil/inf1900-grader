#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.models.assemble import generate_grades_path
from src.models.validate import ensure_not_empty, validate_email_address, validate_grades_path


class MailException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class MailAttachment:
    def __init__(self, type_, path: str, filename: str):
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
    def __init__(self, sender: str, receiver: str, subject: str,
                 message: str = "", attachments: list = []):

        msg = MIMEMultipart()

        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver

        msg.attach(MIMEText(message))

        for attachment in attachments:
            msg.attach(attachment.to_MIME())

        self.msg = msg
        self.sent = False

    def send(self, smtp_addr: str = "smtp.polymtl.ca", port: int = 587):

        if self.sent:
            raise MailException("Mail was already sent!")

        smtp = smtplib.SMTP(smtp_addr, port)
        smtp.send_message(self.msg, self.msg["From"], self.msg["To"])
        smtp.quit()

        self.sent = True


def mail(sender_email: str, recipient_email: str,
         subject: str, message: str, grading_directory: str):
    grades_path = generate_grades_path(grading_directory)

    validate_email_address(sender_email)
    validate_email_address(recipient_email)
    ensure_not_empty(subject, "Subject")
    ensure_not_empty(message, "Message")
    validate_grades_path(grades_path)

    attachment_name = subject.lower().replace(" ", "_")
    attachments = [MailAttachment("text/csv", grades_path, attachment_name)]
    Mail(sender_email, recipient_email, subject, message, attachments).send()
