from typing import Dict, Optional

#Contact class needs to give us
class Contact:
    def __init__(
        self,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        social_media: Optional[Dict[str, str]] = None,
        relationship: Optional[str] = None,
        schedules: Optional[str] = None
    ):
        self.name = name
        self.email = email
        self.phone = phone
        self.social_media = social_media or {}
        self.relationship = relationship  # new field
        self.schedules = schedules # Calendar


    def __repr__(self):
        return (
            f"Contact(name={self.name}, email={self.email}, phone={self.phone}, "
            f"social_media={self.social_media}, relationship={self.relationship})"
        )

    def matches_email(self, email: str) -> bool:
        return self.email and self.email.lower() == email.lower()



class ContactBook:
    def __init__(self):
        self.contacts: Dict[str, Contact] = {}

    def add_contact(self, contact: Contact):
        key = contact.email.lower() if contact.email else contact.name.lower()
        self.contacts[key] = contact

    def get_contact_by_email(self, email: str) -> Optional[Contact]:
        return self.contacts.get(email.lower())

    def get_all_contacts(self):
        return list(self.contacts.values())

    def is_known_contact(self, email: str) -> bool:
        return email.lower() in self.contacts