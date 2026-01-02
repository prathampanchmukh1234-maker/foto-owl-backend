import os, re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
CLIENT_SECRET = "client_secret.json"

def extract_folder_id(url_or_id):
    if "drive.google.com" in url_or_id:
        match = re.search(r"folders/([a-zA-Z0-9_-]+)", url_or_id)
        return match.group(1)
    return url_or_id.strip()

def get_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
    creds = flow.run_console()
    return build("drive", "v3", credentials=creds)

def fetch_images_from_drive(folder_input):
    folder_id = extract_folder_id(folder_input)
    service = get_service()

    results = service.files().list(
        q=f"'{folder_id}' in parents and mimeType contains 'image/'",
        fields="files(id, name, mimeType, size)"
    ).execute()

    return results.get("files", [])
