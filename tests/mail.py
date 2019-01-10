#!/bin/usr/python3

from sys             import argv
from src.models.mail import *

if __name__ == "__main__":

    subject   = "test-mail"
    sender    = argv[1]
    recipient = argv[2]

    while True:

        answer = input(f"Do you want to send {subject} to {recipient} from {sender}? [y/n] ").strip().lower()

        if answer == 'y':
            Mail(sender, recipient, subject, "This is a test message.", []).send()
            break;
        elif answer == 'n':
            break;
        else:
            print("Invalid answer")
