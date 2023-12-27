from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickWindow, QSGRendererInterface


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    views: list[QWebEngineView] = []
    def exit_handler():
        print("exit")
        print(views[0].page().profile().cookieStore().loadAllCookies())
        app.exec()

    for i in range(1):
        webview = QWebEngineView()
        # add browser header

        profile = QWebEngineProfile.defaultProfile()
        profile.setPersistentStoragePath(f"storage-{i}")
        profile.setCachePath(f"storage-{i}")
        profile.setHttpUserAgent("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Safari/537.36")
        profile.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        webpage = QWebEnginePage(profile, webview)
        webview.setPage(webpage)
        # # allow javascript
        webview.load(QUrl("https://affiliates.bybit.com/v2/affiliate-portal/clients?offset=0&coin=All&uid=&page_size=20&business=0"))
        # webview.load(QUrl("https://www.google.com"))
        webview.show()
        views.append(webview)
    sys.exit(exit_handler())