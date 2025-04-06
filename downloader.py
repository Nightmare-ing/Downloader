import sys
import requests
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebEngineWidgets import QWebEngineProfile
from PyQt5.QtCore import QUrl  # Import QUrl
from PyQt5.QtCore import pyqtSignal
import os
import csv

class BrowserWindow(QWebEngineView):
    cookies_ready = pyqtSignal(dict)  # Signal to notify when cookies are ready

    def __init__(self, login_url):
        super().__init__()
        self.login_url = QUrl(login_url)  # Convert string URL to QUrl
        self.cookies = {}
        self.profile = QWebEngineProfile.defaultProfile()
        self.cookie_store = self.profile.cookieStore()
        
        # Connect to the cookieAdded signal to capture cookies as they are added
        self.cookie_store.cookieAdded.connect(self.on_cookie_added)

        # Load the login page
        self.load(self.login_url)  # Use QUrl object

    def on_cookie_added(self, cookie):
        # Convert the QNetworkCookie format to name/value strings
        name = str(cookie.name().data(), 'utf-8')
        value = str(cookie.value().data(), 'utf-8')
        self.cookies[name] = value
        print(f'Cookie added: {name}={value}')
        
    def closeEvent(self, event):
        """
        When the window is closed, emit the cookies_ready signal with the collected cookies.
        """
        super().closeEvent(event)
        self.cookies_ready.emit(self.cookies)  # Emit cookies when the browser is closed

def handle_cookies(cookies):
    """
    Handle the cookies received from the browser and use them to download protected data.
    """
    cookie_jar = {}
    for name, value in cookies.items():
        cookie_jar[name] = value
    download_files(cookie_jar)  # Call the download function with the cookies

def download_files(cookie_jar):
    """
    Download files using the cookies received from the browser.
    """
    download_dir = "outputs"
    os.makedirs(download_dir, exist_ok=True)  # Create download directory if it doesn't exist
    
    with open("links.csv", "r", newline='') as links_file:
        reader = csv.reader(links_file)
        for row in reader:
            filename = row[0]
            download_link = row[1]
            print(f"Processing {filename} with link {download_link}")
            if filename and download_link:
                response = requests.get(download_link, cookies=cookie_jar)
                if response.status_code == 200:
                    target = os.path.join(download_dir, os.path.basename(filename))
                    with open(target, "wb") as f:
                        f.write(response.content)
                    print(f"Downloaded {filename}")
                else:
                    print(f"Failed to download {filename}: {response.status_code}")


def main():
    app = QApplication(sys.argv)
    login_url = "https://github.com"
    browser = BrowserWindow(login_url)
    browser.show()

    browser.cookies_ready.connect(handle_cookies)  # Connect the signal to the handler
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()