# drive_downloader.py
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import os
import pickle
import logging
import re

class DriveDownloader:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.SCOPES = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
        ]
        self.token_file = os.path.join(base_dir, '..', 'config', 'token.pickle')
        self.credentials_file = os.path.join(base_dir, '..', 'config', 'credentials.json')
        self.service = None
        self.folder_id = '1r0-VqI4Lf3cQLnw64ORIE5dcSDbnZaMl'  # ID folderu Drive

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
                    self.credentials_file, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('drive', 'v3', credentials=creds)
        return True

    def download_latest_xml(self, output_dir='data/input_xml'):
        try:
            results = self.service.files().list(
                q=f"'{self.folder_id}' in parents and (mimeType='application/xml' or mimeType='text/xml')",
                orderBy='modifiedTime desc',
                pageSize=1,
                fields='files(id, name)'
            ).execute()
            
            print("Pliki znalezione w folderze:")
            for file in results.get('files', []):
                print(f"- {file['name']} ({file['id']})")
            
            files = results.get('files', [])
            if not files:
                logging.warning(f"No XML files found in folder {self.folder_id}")
                return None
            
            file_id = files[0]['id']
            file_name = files[0]['name']
            
            request = self.service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, file_name)
            
            with open(output_path, 'wb') as f:
                fh.seek(0)
                f.write(fh.read())
            
            logging.info(f"Downloaded: {file_name}")
            return output_path
        
        except Exception as e:
            logging.error(f"Error downloading XML: {e}")
            return None