# Author: Olivier Dion - 2019

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

default_subject = "[DO NOT REPLY] inf1900-grader"

class MailException(Exception):

    def __init__(self, msg):
        super().__init__(msg)

class MailAttachment:

    def __init__(self, type_, filename):

        self.filename = filename

        # Exemple: text/csv
        self.main_type, self.sub_type = type_.split("/")

class Mail:


    # file_ The CSV file to read from
    #
    # from_ Sender of email
    #
    # to_   Receiver of email
    def __init__(self, subject, sender, receiver, attachments=[]):

        msg = MIMEMultipart()

        msg["Subject"] = subject
        msg["From"]    = sender
        msg["To"]      = receiver

        self.filename_list  = []

        for attachment in attachments:

            self.filename_list.append(attachment.filename)

            try:
                with open(attachment.filename, "rb") as f:
                    base = MIMEBase(attachment.main_type,
                                    attachment.sub_type)
                    base.set_payload(f.read())
                    base.add_header("Content-Disposition",
                                    "attachment",
                                    filename=attachment.filename)
                    msg.attach(base)
            except FileNotFoundError as e:
                # TODO
                pass

        self.msg = msg
        self.was_sended = False

    # Connect to smtp_addr:port and send the email
    def send(self, smtp_addr="smtp.polymtl.ca", port=587):

        # We don't want to keep sending the same email by accident
        if self.was_sended:
            raise MailException("Mail was already sent!")

        smtp = smtplib.SMTP(smtp_addr, port)
        smtp.send_message(self.msg, self.msg["From"], self.msg["To"])
        smtp.quit()

        self.was_sended = True
