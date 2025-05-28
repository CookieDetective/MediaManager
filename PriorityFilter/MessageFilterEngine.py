from .rules import match_rules
from .contacts import ContactBook

class MessageFilterEngine:
    def __init__(self, important_contacts=None, keywords=None, contact_book=None):
        self.important_contacts = important_contacts or []
        self.keywords = keywords or [],
        self.contacts = contact_book or ContactBook()

    def analyze_message(self, message):
        """
        Accepts a parsed message (with subject, from, snippet, etc.)
        Returns a tag or priority score.
        """
        sender = message.get("from", "")
        subject = message.get("subject", "")
        snippet = message.get("snippet", "")

        tags = []
        if self.contacts.is_known_contact(sender, self.important_contacts):
            tags.append("important_contact")

        tags += match_rules(subject, snippet, self.keywords)

        return tags