import os.path
import base64
import quopri
import re
import requests
import csv
import io
import google_utils

from kyte_process import extract_url, extract_data

from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", 'https://www.googleapis.com/auth/drive', "https://www.googleapis.com/auth/spreadsheets"]


def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """

  credentials = google_utils.auth_google(SCOPES)

  try:
    last_message = google_utils.get_last_gmail(credentials)
    #TODO: Validate if is a valid kyte message or look for the last kyte message
    url = extract_url(last_message)
    data = extract_data(requests.get(url))
    print(url)
    main_file_id = "1va3pv0Lu-AoHhTUMG-A58Dd99BrGoVeDNp8naYRTEjU"  #TODO "save id in ENV"
    new_name = f"{datetime.now().strftime("%d/%m")} ventas"
    new_file = google_utils.duplicate_file(credentials, main_file_id, new_name)
    email = "miky116@gmail.com" #TODO Environment
    google_utils.add_user_writer_permission(credentials, new_file["id"], email)
    destination = "Data!A1" #TODO ENV
    #print(data)
    google_utils.insert_data_in_sheet(credentials, new_file["id"], data, destination)

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()