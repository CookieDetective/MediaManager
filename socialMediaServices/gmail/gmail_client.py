# services/gmail/gmail_client.py

import os.path
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from langchain.chat_models import ChatOpenAI

import yaml

class GmailClient:
    def __init__(self):
        with open("config/settings.yaml") as f:
            config = yaml.safe_load(f)["gmail"]
        self.token_file = config["token_file"]
        self.credentials_file = config["credentials_file"]
        self.scopes = config["scopes"]

        self.service = None
        self.creds = None

    def login(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.scopes)
                self.creds = flow.run_local_server(port=0)
            with open(self.token_file, 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('gmail', 'v1', credentials=self.creds)

    def read_emails(self, max_results=5):
        if not self.service:
            raise RuntimeError("Not logged in")

        results = self.service.users().messages().list(userId='me', maxResults=max_results).execute()
        messages = results.get('messages', [])
        emails = []

        for msg in messages:
            msg_data = self.service.users().messages().get(userId='me', id=msg['id']).execute()
            snippet = msg_data.get('snippet', '')
            emails.append(snippet)
        return emails

    def respond_to_email(self, prompt: str):
        llm = ChatOpenAI(temperature=0)
        response = llm.predict(prompt)
        return response