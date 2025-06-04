from manager.media_references import MediaReferences
from datetime import timedelta

class CommandRouter:
    def __init__(self, manager):
        self.manager = manager
        self.ref_manager = MediaReferences()

    def route(self, input_text: str):
        # Get structured response from ReferenceManager
        response = self.ref_manager.infer_action(input_text)
        action = response.get("action")
        data = response.get("data", {})
        clarification = response.get("clarify")
        clarification_action = response.get("clarification_action")

        # If clarification is needed, ask before continuing
        if clarification:
            if clarification_action:
                confirm = input(clarification + "(y/n) >").strip().lower()
                if confirm != 'y':
                    print("cancelled")
                    return
                #Implement code to do action ++++++
            else:
                print(clarification)
                confirm = input(" Do you want to cancel? (y/n) ").strip().lower()
                if confirm == 'y':
                    print("Cancelled.")
                    return

        # Route based on action
        if action == "calendar_event":
            self._handle_calendar_event(data)
        elif action == "email_draft":
            self._handle_email_draft()
        elif action == "add_contact":
            self._handle_add_contact(data)
        else:
            print("Sorry, I couldn’t understand that command.")

    def _handle_calendar_event(self, data):
        dt = data.get("datetime")
        if not dt:
            print("⚠️ No datetime found.")
            return
        title = input("Event title: ")
        self.manager.calendar.create_event(
            summary=title,
            start_time=dt.isoformat(),
            end_time=(dt + timedelta(hours=1)).isoformat()
        )
        print("✅ Calendar event created.")

    def _handle_email_draft(self):
        to = input("To: ")
        subject = input("Subject: ")
        body = input("Body:\n")
        self.manager.save_draft(to=to, subject=subject, body=body)
        print("✅ Email draft saved.")

    def _handle_add_contact(self, data):
        name = data.get("name") or input("Name: ")
        email = data.get("email") or input("Email: ")
        note = data.get("note") or input("Relationship note: ")
        self.manager.contacts.add_contact(name=name, email=email, note=note)
        print("👥 Contact added.")