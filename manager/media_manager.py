from socialMediaServices.gmail.gmail_client import GmailClient
from PriorityFilter.contacts import ContactBook
from PriorityFilter.MessageFilterEngine import MessageFilterEngine


class MediaManager:
    def __init__(self):
        self.gmail = GmailClient()
        self.contacts = ContactBook()

    def login(self):
        self.gmail.login()

    def logout(self):
        self.gmail.logout()

    def list_emails(self):
        return self.gmail.search_emails("")

    def filter_emails(self, keywords=None):
        emails = self.list_emails()
        engine = MessageFilterEngine(contact_book=self.contacts, keywords=keywords or [])
        important = []

        for email in emails:
            tags = engine.analyze_message(email)
            if tags:
                important.append((email, tags))

        return important

    def add_contact(self, contact):
        self.contacts.add_contact(contact)

    def save_draft(self, to, subject, body):
        self.gmail.create_draft(to=to, subject=subject, message_text=body)