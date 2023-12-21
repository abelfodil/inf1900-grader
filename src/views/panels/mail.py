from urwid import Edit, LineBox

from src.models.mail import mail
from src.models.state import state
from src.views.widgets.form import Form


class MailPanel(Form):

    def __init__(self):
        sender = LineBox(Edit(("header", "Sender email\n\n"), state.sender_email))
        recipient = LineBox(Edit(("header", "Recipient email\n\n"), state.recipient_email))
        grading_directory = LineBox(Edit(("header", "Grading directory\n\n"), state.grading_directory))
        subject = LineBox(Edit(("header", "Subject\n\n"), state.subject))
        message = LineBox(Edit(("header", "Message\n\n"), state.message, multiline=True))

        username = LineBox(Edit(("header", "Username\n\n"), ""))
        password = LineBox(Edit(("header", "Password\n\n"), "", mask="*"))

        grid_elements = [
            {"grading_directory": grading_directory, "subject": subject},
            {"sender_email": sender, "recipient_email": recipient},
            {"username": username, "password": password},
            {"message": message},
        ]

        super().__init__("Mail", grid_elements, mail)
