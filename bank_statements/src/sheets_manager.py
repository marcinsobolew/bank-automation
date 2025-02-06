from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle

class SheetsManager:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.token_file = os.path.join(base_dir, 'config', 'token.pickle')
        self.credentials_file = os.path.join(base_dir, 'config', 'credentials.json')

    def authenticate(self):
        creds = None
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)
        return True

    def update_sheet(self, data, spreadsheet_id, range_name='Sheet1'):
        try:
            values = [list(data.columns)]  # Headers
            values.extend(data.values.tolist())  # Data

            body = {
                'values': values
            }
            result = self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            print(f"{result.get('updatedCells')} cells updated.")
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False