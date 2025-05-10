from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
import os.path
import io
import requests

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
MIMETYPES = {"pdf": "application/pdf",
             "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation"}

def main():
    """
    Shows basic usage of the Drive v3 API.
    Downloads a file from Google Drive.
    """
    service = create_service()
    # doc_link1 = "https://docs.google.com/presentation/d/1ADK25v7v3HaATJETk5W9NSWvRA_Y18WDLsgkphWHzCI/edit?usp=share_link"
    # doc_link = "https://docs.google.com/presentation/d/1hRUkaONWvWP7IZbINLP-G6uOyyulDqury5kop7638co"
    file_link = "https://drive.google.com/file/d/10TBXmYiDwyN4hIBEctfuRYDqyZyotDOn/view?usp=sharing"
    # file_link1 = "https://drive.google.com/file/d/1ZQleDXUF7Y_6_Faff4PtB0zmERvQ14u5/view?usp=sharing"

    # doc_id1 = parse_link(doc_link1)
    # doc_id = parse_link(doc_link)
    file_id = parse_link(file_link)


    # download_pres_with_id(doc_id, service)
    # download_pres_with_id(doc_id1, service)
    download_file_with_id(file_id, os.path.join(os.getcwd(), "outputs", file_id + ".pdf"))


def parse_link(link):
    """
    Parse the Google Drive link to extract the file ID.
    """
    file_id = None
    if "drive.google.com" in link:
        file_id = link.split('/')[-2]
    elif "docs.google.com/presentation" in link:
        if "edit" in link:
            file_id = link.split('/')[-2]
        else:
            file_id = link.split('/')[-1]
        return file_id
    else:
        raise ValueError("Invalid Google Drive link")
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
    return service


def download_pres_with_id(file_id, service, types=["pptx", "pdf"]):
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
            file_path = os.path.join(os.getcwd(), "outputs", file_name + "." + file_type)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            print(f"Downloading {file_name} as {file_type}...")
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%.")
            # Save the file locally
            with open(file_path, 'wb') as f:
                f.write(fh.getvalue())
            print(f'File downloaded as {file_path}')
    except HttpError as error:
        print(f'An error occurred: {error}')


def download_file_with_id(file_id, path):
    """
    Download a Google Doc file using its file ID.
    """
    URL = "https://drive.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)
    
    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    
    save_response_content(response, path)


def get_confirm_token(response):
    """
    Get the confirmation token from the response.
    """
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None


def save_response_content(response, path):
    """
    Save the response content to a file.
    """
    CHUNK_SIZE = 32768
    with open(path, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)
    print(f"File downloaded to {path}")



if __name__ == '__main__':
    main()