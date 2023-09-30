import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
import json
load_dotenv()


class GoogleDriveUploader:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.SERVICE_ACCOUNT_JSON = os.getenv('SERVICE_ACCOUNT')
        self.PARENT_FOLDER_ID = os.getenv('ID')

    def authenticate(self):
        creds = service_account.Credentials.from_service_account_info(
            info=json.loads(self.SERVICE_ACCOUNT_JSON), scopes=self.SCOPES)
        return creds

    def upload_photo(self, file_name, file_path):
        creds = self.authenticate()
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': file_name,
            'parents': [self.PARENT_FOLDER_ID]
        }

        file = service.files().create(
            body=file_metadata,
            media_body=file_path
        ).execute()

        # Retrieve the web view link of the uploaded file
        web_view_link = file.get('webViewLink')

        return web_view_link
