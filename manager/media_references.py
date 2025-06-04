import re
import datetime
from dateutil import parser as date_parser

#Manages the actions and flow for when the bot is focused on interacting with: gmail, calendar
class MediaReferences:
    def __init__(self):
        pass

    def infer_action(self, user_input: str):
        user_input = user_input.lower()
        #Store responses in dictionaries
        #Initialize a data dictionary and then we will have other common ones such as 'action' or 'clarify'
        response = {"data": {}}

        # Calendar example: "Friday at 7 PM"
        #Expand upon the searches here, create list of days/months/holidays ++++++
        time_match = re.search(r"(?:on\s)?(friday|monday|tuesday|wednesday|thursday|saturday|sunday).*?(\d{1,2}(?::\d{2})?\s*(?:am|pm))", user_input)
        if time_match:
            try:
                day = time_match.group(1)
                time = time_match.group(2)
                dt = date_parser.parse(f"{day} {time}", fuzzy=True)
                response["action"] = "calendar_event"
                response["data"]["datetime"] = dt
                response["clarify"] = f"Do you want me to set an event for {dt.strftime('%A at %I:%M %p')} in your calendar?"
                return response
            except:
                pass

        # Email example: "Email my professor" or "send a message"
        #Expand into classes/managers  that can associate contacts with preferred methods of contact ++++++
        #ex. Dr. - Email, Guy from bar - instagram
        if "email" in user_input or "message" in user_input:
            response["action"] = "email_draft"
            response["clarify"] = "Do you want to draft a new email?"
            return response

        # Contact example
        if "add contact" in user_input or "new friend" in user_input:
            response["action"] = "add_contact"
            response["clarify"] = "Do you want to add a new contact?"
            return response

        return response
