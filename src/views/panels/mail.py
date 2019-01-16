from urwid import Edit, LineBox

from src.models.mail import mail
from src.models.state import state
from src.views.base.form import Form
from src.views.base.signal import Signal, SignalType
from src.views.panels.abstract import AbstractPanel


@Signal(SignalType.QUIT)
class MailPanel(AbstractPanel):

    def __init__(self):
        sender = LineBox(Edit(("header", "Sender email\n\n"), state.sender_email))
        recipient = LineBox(Edit(("header", "Recipient email\n\n"), state.recipient_email))
        grading_directory = LineBox(
            Edit(("header", "Grading directory\n\n"), state.grading_directory))
        subject = LineBox(Edit(("header", "Subject\n\n"), state.subject))
        message = LineBox(Edit(("header", "Message\n\n"), state.message, multiline=True))

        grid_elements = [
            [sender, recipient],
            [grading_directory, subject],
            [message],
        ]

        form = Form(mail,
                    sender_email=sender,
                    recipient_email=recipient,
                    subject=subject,
                    message=message,
                    grading_directory=grading_directory)

        super().__init__(grid_elements, form)
