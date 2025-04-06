import sys
from PyQt5.QtWidgets import QApplication
from browser import BrowserWindow
import os
import csv
import requests
import shutil


def dload_with_cookies(cookies):
    """
    Use cookies to download protected data.
    """
    dload_dir = "outputs"
    os.makedirs(dload_dir, exist_ok=True)
    
    with open("links.csv", "r", newline='') as links_file:
        reader = csv.reader(links_file)
        for row in reader:
            target_name = row[0]
            target_link = row[1]
            print(f"Processing {target_name} with link {target_link}")

            if target_name and target_link:
                response = requests.get(target_link, cookies=cookies)
                if response.status_code == 200:
                    target = os.path.join(dload_dir, os.path.basename(target_name))
                    with open(target, "wb") as f:
                        f.write(response.content)
                    print(f"Downloaded {target_name}")
                else:
                    print(f"Failed to download {target_name}: {response.status_code}")

    # Create a zip file of the downloaded files
    shutil.make_archive(dload_dir, 'zip', dload_dir)

def main():
    app = QApplication(sys.argv)
    login_url = "https://github.com"
    browser = BrowserWindow(login_url)
    browser.show()
    browser.cookies_ready.connect(dload_with_cookies)  # Connect the signal to the handler
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()