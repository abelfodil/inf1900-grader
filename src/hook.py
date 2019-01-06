# Olivier Dion - 2019

from src.hydra import Hydra
from src.mail  import Mail


def hook_mail(state):

    mail = Mail()

    mail_heads = [
        ("y", lambda:)
    ]
