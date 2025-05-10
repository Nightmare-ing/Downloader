from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
import os.path
import io

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def main():
    """
    Shows basic usage of the Drive v3 API.
    Downloads a file from Google Drive.
    """
    creds = get_creds()
    link = "https://docs.google.com/presentation/d/1hRUkaONWvWP7IZbINLP-G6uOyyulDqury5kop7638co"
    file_id = link.split('/')[-1]
    download_docs_with_id(file_id, creds)


def get_creds():
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
    return creds


def download_docs_with_id(file_id, creds):
    """
    Download a Google Doc file using its file ID.
    """
    try:
        # Call the Drive v3 API
        service = build('drive', 'v3', credentials=creds)

        # The ID of the file you want to export
        file_metadata = service.files().get(fileId=file_id).execute()
        file_name = file_metadata.get('name')
        request = service.files().export_media(fileId=file_id,
                                               mimeType='application/vnd.openxmlformats-officedocument.presentationml.presentation')
        file_path = os.path.join(os.getcwd(), "outputs", file_name + ".pptx")
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")

        # Save the file locally
        with open(file_path, 'wb') as f:
            f.write(fh.getvalue())
        print(f'File downloaded as {file_path}')
    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()