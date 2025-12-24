import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def extract_folder_id(url):
    match = re.search(r"folders/([a-zA-Z0-9_-]+)", url)
    if not match:
        raise ValueError("Invalid Google Drive folder URL")
    return match.group(1)

def fetch_images_from_drive(folder_url):
    folder_id = extract_folder_id(folder_url)

    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("drive", "v3", credentials=creds)

    results = service.files().list(
        q=f"'{folder_id}' in parents and mimeType contains 'image/'",
        fields="files(id, name, mimeType, size)"
    ).execute()

    return results.get("files", [])
