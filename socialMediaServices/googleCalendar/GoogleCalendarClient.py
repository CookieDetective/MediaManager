import os
import datetime
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendarClient:
    def __init__(self, creds_file='token_calendar.json'):
        self.creds = None
        self.creds_file = creds_file
        self.service = None

    def login(self):
        if os.path.exists(self.creds_file):
            self.creds = Credentials.from_authorized_user_file(self.creds_file, SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                client_config = {
                    "installed": {
                        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": ["http://localhost"]
                    }
                }
                flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open(self.creds_file, 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('calendar', 'v3', credentials=self.creds)

    def list_upcoming_events(self, max_results=10):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = self.service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=max_results, singleEvents=True,
            orderBy='startTime').execute()
        return events_result.get('items', [])

    def create_event(self, summary, start_time, end_time, description=None, timezone='UTC'):
        event = {
            'summary': summary,
            'description': description or '',
            'start': {'dateTime': start_time, 'timeZone': timezone},
            'end': {'dateTime': end_time, 'timeZone': timezone},
        }
        return self.service.events().insert(calendarId='primary', body=event).execute()

    def search_events_by_keywords(self, keywords, max_results=50):
        """
        Search for upcoming events that contain specific keywords in their summary or description.

        Args:
            keywords (list[str]): A list of keywords to match (case-insensitive).
            max_results (int): Max number of events to fetch before filtering.

        Returns:
            list[dict]: Events matching any of the keywords.
        """
        keywords = [kw.lower() for kw in keywords]
        events = self.list_upcoming_events(max_results=max_results)

        matching_events = []
        for event in events:
            summary = event.get('summary', '').lower()
            description = event.get('description', '').lower()
            if any(kw in summary or kw in description for kw in keywords):
                matching_events.append(event)

        return matching_events