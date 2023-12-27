from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QCoreApplication, QEvent, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtNetwork import QNetworkCookie
from PySide6.QtCore import QDateTime, QUrl
from bs4 import BeautifulSoup

from constants.keymap import KEYMAP

class CoreBrowser(QWebEngineView):
    def __init__(self):
        self.bs4: BeautifulSoup = None
        super().__init__()
       

    def send_keys(self, text: str):
        for letter in text:
            key = KEYMAP.get(letter.lower(), Qt.Key_unknown)
            event = QKeyEvent(QEvent.KeyPress, key, Qt.NoModifier, letter)
            QCoreApplication.postEvent(self.focusProxy(), event)
    
    def check_login_required(self):
        return 'login' in self.url().toString()
    
    def focus_element(self, selector: str, cb: callable = None):
        self.page().runJavaScript(f"document.querySelector('{selector}').focus();",0, cb)
    
    def get_element(self, selector: str, cb: callable = None):
        self.page().runJavaScript(f"document.querySelector('{selector}');",0, cb)

    def click_element(self, selector: str, cb: callable = None):
        self.page().runJavaScript(f"document.querySelector('{selector}').click();",0, cb)
    
    def on_load(self, cb: callable = None):
        html = self.page().toHtml(lambda html: cb(html))
        if(html):
            self.bs4 = BeautifulSoup(html, "html.parser")
        self.loadFinished.connect(cb)

    def set_page_html(self, cb: callable = None):
        self.page().toHtml(lambda html: self.set_bs4(html, cb))

    def set_bs4(self, html: str, cb: callable = None):
        # print(html)
        self.bs4 = BeautifulSoup(html, "html.parser")
        if(cb is None):
            return
        cb()

    def on_url_changed(self, cb: callable = None):
        if(cb is None):
            return
        self.urlChanged.connect(cb)

    def on_rendered(self, cb: callable = None):
        self.renderProcessTerminated.connect(cb)

    def go_to(self, url: str, cb: callable = None):
        self.load(QUrl(url))
        self.on_load(cb)

        