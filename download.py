import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication
from browser import BrowserWindow
import os
import csv
import requests
import shutil


def download_with_cookies(cookies):
    """
    Use cookies to download protected data.
    """
    download_dir = "outputs"
    os.makedirs(download_dir, exist_ok=True)
    
    with open("links.csv", "r", newline='') as links_file:
        reader = csv.reader(links_file)
        for row in reader:
            target_name = row[0]
            target_link = row[1]
            print(f"Processing {target_name} with link {target_link}")

            if target_name and target_link:
                response = requests.get(target_link, cookies=cookies)
                if response.status_code == 200:
                    target = os.path.join(download_dir, os.path.basename(target_name))
                    with open(target, "wb") as f:
                        f.write(response.content)
                    print(f"Downloaded {target_name}")
                else:
                    print(f"Failed to download {target_name}: {response.status_code}")

    # Create a zip file of the downloaded files
    shutil.make_archive(download_dir, 'zip', download_dir)
    print("Thank you for downloading the files! Have a great day!")

def main():
    if len(sys.argv) < 2:
        print("Usage: python download.py <login_url>")
        sys.exit(1)
    
    QCoreApplication.setApplicationName("Link Downloader")
    app = QApplication(sys.argv)
    login_url = sys.argv[1]  # Get the login URL from command line arguments
    browser = BrowserWindow(login_url)
    browser.show()
    browser.cookies_ready.connect(download_with_cookies)  # Connect the signal to the handler
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()