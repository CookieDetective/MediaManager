
from socialMediaServices.gmail.gmail_client import GmailClient

class MediaManager:
    def __init__(self):
        self.gmail = GmailClient()

    def login_gmail(self):
        self.gmail.login()

    def logout_gmail(self):
        self.gmail.logout()