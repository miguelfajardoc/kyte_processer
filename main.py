import requests
import google_utils
import os.path
import time

from kyte_process import extract_url, extract_data

from datetime import datetime
from googleapiclient.errors import HttpError



# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", 'https://www.googleapis.com/auth/drive', "https://www.googleapis.com/auth/spreadsheets"]


def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  google_utils.get_credentials_from_env_variables()
  if os.getenv("CREDS_FROM_TOKEN"):
    google_utils.get_token_from_env_variables()

  time.sleep(5)
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
    emails = os.getenv("PERMISSION_EMAILS")
    emails = emails.split(', ') if emails else print(f'Invalid emails')
    google_utils.add_user_writer_permission(credentials, new_file["id"], emails)
    destination = "Data!A1" #TODO ENV
    #print(data)
    google_utils.insert_data_in_sheet(credentials, new_file["id"], data, destination)

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()