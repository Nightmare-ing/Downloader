from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
import os.path
import io
import requests
import logging

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
MIMETYPES = {"pdf": "application/pdf",
             "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
             "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}

def main():
    """
    Shows basic usage of the Drive v3 API.
    Downloads a file from Google Drive.
    """
    creds, service = create_service()
    # doc_link1 = "https://docs.google.com/presentation/d/1ADK25v7v3HaATJETk5W9NSWvRA_Y18WDLsgkphWHzCI/edit?usp=share_link"
    # doc_link = "https://docs.google.com/presentation/d/1hRUkaONWvWP7IZbINLP-G6uOyyulDqury5kop7638co"
    file_link = "https://drive.google.com/file/d/10TBXmYiDwyN4hIBEctfuRYDqyZyotDOn/view?usp=sharing"
    # file_link1 = "https://drive.google.com/file/d/1ZQleDXUF7Y_6_Faff4PtB0zmERvQ14u5/view?usp=sharing"

    # doc_id1 = parse_link(doc_link1)
    # doc_id = parse_link(doc_link)
    file_id = get_file_id(file_link)


    # download_pres_with_id(doc_id, service)
    # download_pres_with_id(doc_id1, service)
    download_file_with_id(file_id, creds)


def get_file_id(link):
    """
    Parse the Google Drive link to extract the file ID.
    """
    file_id = None
    if "drive.google.com" in link:
        if "file/d/" in link:
            file_id = link.split('/')[-2]
        elif "open?id=" in link:
            file_id = link.split('=')[-1]
        elif "folders" in link:
            logging.error("Google Drive folder links: {link} are not supported.")
        else:
            logging.error("Invalid Google Drive link: {link}.")
    elif "docs.google.com/presentation" in link:
        if "edit" in link:
            file_id = link.split('/')[-2]
        else:
            file_id = link.split('/')[-1]
    elif "docs.google.com/document" in link:
        if "edit" in link:
            file_id = link.split('/')[-2]
        else:
            file_id = link.split('/')[-1]
    else:
        logging.error("Invalid Google Docs link: {link}.")
    return file_id


def create_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    # Call the Drive v3 API
    service = build('drive', 'v3', credentials=creds)
    return creds, service


def download_docs_with_id(storage_path, file_id, service, types=["pptx", "pdf"]):
    """
    Download a Google Doc file using its file ID.
    """
    try:
        # The ID of the file you want to export
        file_metadata = service.files().get(fileId=file_id).execute()
        file_name = file_metadata.get('name')
        for file_type in types:
            request = service.files().export_media(fileId=file_id,
                                                   mimeType=MIMETYPES[file_type])
            file_path = os.path.join(storage_path, file_name + "." + file_type)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            logging.info(f"Downloading {file_name} as {file_type}...")
            while done is False:
                status, done = downloader.next_chunk()
                logging.info(f"Download {int(status.progress() * 100)}%.")
            # Save the file locally
            with open(file_path, 'wb') as f:
                f.write(fh.getvalue())
            logging.info(f"File downloaded as {file_path}")
    except HttpError as error:
        logging.error(f"An error occurred: {error}")


def download_file_with_id(storage_path, file_id, creds, file_type="pdf"):
    """
    Download a Google Doc file using its file ID.
    """
    headers = {"Authorization": "Bearer " + creds.token}
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        file_name = file_id + "." + file_type
        file_path = os.path.join(storage_path, file_name)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        logging.info(f"File downloaded as {file_path}")
    else:
        logging.error(f"An error occurred: {response.status_code}")


if __name__ == '__main__':
    main()