from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

# file_id = "1hdWYTHP5P7QXnVO9-RoE3iNj5QEbb9eT"
file_id = "1TA-xr-z7df4vnJz6oo4s7OkpGLoVy1EYYTwR_8AVhxA"
file = drive.CreateFile({"id": file_id})

# file.GetContentFile("outputs/test.mp4")
file.GetContentFile("outputs/test.pptx")
print("Files downloaded successfully.")