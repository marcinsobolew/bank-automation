from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle

class SheetsManager:
   def __init__(self):
       self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
       base_dir = os.path.dirname(os.path.abspath(__file__))
       self.token_file = os.path.join(base_dir, '..', 'config', 'token.pickle')
       self.credentials_file = os.path.join(base_dir, '..', 'config', 'credentials.json')
       self.service = None

   def authenticate(self):
       self.SCOPES = [
           'https://www.googleapis.com/auth/spreadsheets',
           'https://www.googleapis.com/auth/drive.readonly'
       ]
       
       creds = None
       if os.path.exists(self.token_file):
           with open(self.token_file, 'rb') as token:
               creds = pickle.load(token)
       
       if not creds or not creds.valid:
           if creds and creds.expired and creds.refresh_token:
               creds.refresh(Request())
           else:
               flow = InstalledAppFlow.from_client_secrets_file(
                   self.credentials_file, 
                   scopes=self.SCOPES
               )
               creds = flow.run_local_server(port=0)
           
           with open(self.token_file, 'wb') as token:
               pickle.dump(creds, token)
       
       self.service = build('sheets', 'v4', credentials=creds)
       return True

   def update_sheet(self, data, spreadsheet_id, range_names=['statement!A1']):
       for range_name in range_names:
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
               print(f"{result.get('updatedCells')} cells updated in {range_name}")
               return True
           except Exception as e:
               print(f"Failed to update {range_name}: {e}")
               if range_name == range_names[-1]:
                   print(f"All sheet names failed")
                   return False
               continue