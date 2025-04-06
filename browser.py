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
