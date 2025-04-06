import sys
import requests
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebEngineWidgets import QWebEngineProfile
from PyQt5.QtCore import QUrl  # Import QUrl
from PyQt5.QtCore import pyqtSignal

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

    protected_url = "https://github.com/Nightmare-ing/EECS151-Fa20/archive/refs/heads/master.zip"
    response = requests.get(protected_url, cookies=cookie_jar)
    if response.status_code == 200:
        print("Download protected data successfully.")
        with open("EECS151-master.zip", "wb") as f:
            f.write(response.content)
        print("Protected data saved as 'EECS151-master.zip'")
    else:
        print(f"Failed to download protected data {response.status_code}")

def main():
    app = QApplication(sys.argv)
    login_url = "https://github.com"
    browser = BrowserWindow(login_url)
    browser.show()

    browser.cookies_ready.connect(handle_cookies)  # Connect the signal to the handler
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()