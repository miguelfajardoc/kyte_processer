import os.path

from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def auth_google(scopes):
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", scopes
            )
            creds = flow.run_local_server(port=8080, access_type='offline', prompt='consent')
            # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def get_last_gmail(credentials):
    service = build("gmail", "v1", credentials=credentials)
    results = (
        service.users().messages().list(userId="me", labelIds=["INBOX"]).execute()
    )
    messages = results.get("messages", [])
    if not messages:
        print("No messages found.")
        return
    msg = (
            service.users().messages().get(userId="me", id=messages[0]["id"]).execute()
        )
    return msg
  
def duplicate_file(credentials, id, new_name="default"):
    body = {
        'name': new_name
    }
    service = build("drive", "v3", credentials=credentials)
    files = search_file(service, new_name)
    if files != None:
        for file in files:
            print(f"Eliminando archivo: {file['name']} (ID: {file['id']})")
            service.files().delete(fileId=file["id"]).execute()

    return service.files().copy(fileId=id, body=body).execute()

def search_file(service, file_name):
    query = f"name = '{file_name}' and trashed = false"
    results = service.files().list(
        q=query,
        spaces="drive",
        fields="files(id, name)",
        pageSize=10
    ).execute()

    files = results.get("files", [])

    if not files:
        return None
    else:
        return files

def add_user_writer_permission(credentials, id, email):
    service = build("drive", "v3", credentials=credentials)
    service.permissions().create(
      fileId=id,
      body={'type': 'user', 'role': 'writer', 'emailAddress': email},
      fields='id',
      sendNotificationEmail=False
    ).execute()

def insert_data_in_sheet(credentials, id, data, destination):
    service_sheet = build("sheets", "v4", credentials=credentials)
    return service_sheet.spreadsheets().values().update(
      spreadsheetId=id,
      range=destination,
      valueInputOption="USER_ENTERED",
      body={'values': data}
    ).execute()