import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import listdir
from os.path import basename, isfile, join

from src.models.validate import InvalidInput, ensure_grading_directory_exists, ensure_not_empty, \
    validate_email_address


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


def get_grade_file_path(grading_directory: str):
    grades_files = [join(grading_directory, file) for file in listdir(grading_directory)
                    if isfile(join(grading_directory, file)) and file.endswith(".csv")]

    if len(grades_files) < 1:
        raise InvalidInput(f"No grades file found. "
                           f"Please make sure to assemble grades first.")

    return grades_files[0]


def mail(sender_email: str, recipient_email: str,
         subject: str, message: str, grading_directory: str):
    ensure_grading_directory_exists(grading_directory)
    validate_email_address(sender_email)
    validate_email_address(recipient_email)
    ensure_not_empty(subject, "Subject")
    ensure_not_empty(message, "Message")

    grades_file = get_grade_file_path(grading_directory)
    attachment_name = basename(grades_file)
    attachments = [MailAttachment("text/csv", grades_file, attachment_name)]
    Mail(sender_email, recipient_email, subject, message, attachments).send()
