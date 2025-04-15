import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication
from browser import BrowserWindow
import os
import csv
import requests
import shutil
import argparse


def main():
    args = parse_args()
    QCoreApplication.setApplicationName("Link Downloader")
    app = QApplication(sys.argv)
    login_url = args.url  # Get the login URL from command line arguments
    links_file = args.file # Get the file containing links from command line arguments
    browser = BrowserWindow(login_url)
    browser.show()

    browser.cookies_ready.connect(lambda cookies: download_with_cookies(cookies, links_file))  # Connect the signal to the handler
    sys.exit(app.exec_())


def parse_args():
    """
    Parse command line arguments.
    """
    if len(sys.argv) < 5:
        print("Usage: python download.py --file <links.csv> --url <login_url>")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description="Download files using cookies.")
    parser.add_argument('-f', '--file', type=str, required=True, help='Path to the CSV file containing links.')
    parser.add_argument('-u', '--url', type=str, required=True, help='Login URL for authentication.')
    return parser.parse_args()
    

def download_with_cookies(cookies, links_file):
    """
    Use cookies to download protected data.
    """
    download_dir = "outputs"
    os.makedirs(download_dir, exist_ok=True)
    
    with open(links_file, "r", newline='') as links_file:
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


if __name__ == '__main__':
    main()