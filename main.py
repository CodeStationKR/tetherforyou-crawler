import json
import re
import sys
import time
from PySide6.QtCore import QTimer, QUrl
from PySide6.QtWidgets import QApplication, QMainWindow
import requests
from modules.core_browser import CoreBrowser
from constants.accounts import BY_BIT_ACCOUNT

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.browser = CoreBrowser()
        self.browser.load(
            QUrl(f"https://affiliates.bybit.com/v2/affiliate-portal/login?next=%2Fclients%3Foffset%3D0%26coin%3DAll%26uid%3D%26page_size%3D20%26business%3D0")
        )
        self.setCentralWidget(self.browser)

        # add label in window

        self.browser.on_load(self.handle_load_finished)
        self.browser.on_url_changed(self.handle_url_changed)
        self.browser.on_rendered(self.handle_rendered)

    def handle_rendered(self, *args):
        print("Rendered")

    def handle_load_finished(self, ok):
        if ok:
            if self.browser.check_login_required():
                QTimer.singleShot(100, self.write_email)
            print("Page loaded")
        else:
            print("Could not load page")

    def handle_url_changed(self, url: QUrl):
        if (url.toString() == 'https://affiliates.bybit.com/v2/affiliate-portal/clients?offset=0&coin=All&uid=&page_size=20&business=0'):
            print('now!!')
            QTimer.singleShot(2000, self.run)

    def write_email(self, *args):
        self.browser.focus_element("#login_email", self.callback_email)

    def callback_email(self, *args):
        self.browser.send_keys(BY_BIT_ACCOUNT["email"])
        QTimer.singleShot(100, self.write_password)

    def write_password(self):
        self.browser.focus_element(
            '#login_password',  
            self.callback_password,
        )

    def callback_password(self, *args):
        self.browser.send_keys(BY_BIT_ACCOUNT["password"])
        QTimer.singleShot(200, self.click)

    def click(self):
        self.browser.page().runJavaScript(
            """let btn = document.querySelector('div.ant-form-item-control-input-content button');
                btn.focus();
                btn.click();"""
        )
    
    def run(self):
        self.browser.set_page_html(
            self.callback_run,
        )

    def preprocess(self, total_trade: str):
        total_trade = re.sub('[^0-9.]', '', total_trade)
        if(total_trade == ''):
            total_trade = 0.0
        total_trade = float(total_trade)
        if(total_trade < 0):
            total_trade = -total_trade
        return total_trade
    
    def get_base_url(self, start_date, end_date, page):
        return f'https://affiliates.bybit.com/v2/affiliate-portal/clients?offset=0&coin=All&uid=&page_size=20&start_date={start_date}&end_date={end_date}&business=0&page={page}'
    


    def callback_run(self, *args):

        print('Bybit 크롤링을 시작합니다.')
        two_days_ago = time.strftime('%Y-%m-%d', time.localtime(time.time() - 60 * 60 * 24 * 2))
        yesterday = time.strftime('%Y-%m-%d', time.localtime(time.time() - 60 * 60 * 24))
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        days = [two_days_ago, yesterday, today]

        self.browser.set_page_html()
        time.sleep(1)
        total_pages_h5 = self.browser.bs4.select('div.clients-page-table-panel > h5.ant-typography')[0].text.replace(' Results', '')
        total_pages = int(total_pages_h5)
        total_page = total_pages // 20 + 1
        print(total_page)
        for page in range(1, total_page + 1):
            url = self.get_base_url(days[0], days[0], page)
            self.browser.go_to(url, self.callback_go_to(days[0]))

            url = self.get_base_url(days[1], days[1], page)
            self.browser.go_to(url, self.callback_go_to(days[1]))

            url = self.get_base_url(days[2], days[2], page)
            self.browser.go_to(url, self.callback_go_to(days[2]))
            time.sleep(1)
        print('Bybit 크롤링을 종료합니다.')
        self.browser.close()
            

    def callback_go_to(self, date):
        self.browser.set_page_html()
        time.sleep(1)
        results = []
        table = self.browser.bs4.select('div.ant-table-content > table')[0]
        tbody = table.select('tbody')[0]
        trs = tbody.select('tr')
        
        for tr in trs[1:]:
            tds = tr.select('td')
            uid = tds[0].text.replace('\n', '').replace(' ', '')
            settled_commission = tds[1].text
            settled_commission = settled_commission.split(' USDT')[0]
            settled_commission = self.preprocess(settled_commission)    
            total_trade = tds[-3].text
            if('\n' in total_trade):
                total_trades = total_trade.split('\n')
                total = 0.0
                for total_trade in total_trades:
                    total_trade = self.preprocess(total_trade)
                    total += total_trade
                results.append({
                    'uid': uid,
                    'transaction': total,
                    'payback': settled_commission * 0.9,
                    'date': date
                })
            else:
                total_trade = self.preprocess(total_trade)
                results.append({
                    'uid': uid,
                    'transaction': total_trade,
                    'payback': settled_commission * 0.9,
                    'date': date
                })
        print(results)
        self.upload(results)

    def upload(self, results):
        data = {
            'reqs': results
        }
        req_json = json.dumps(data)
        response = requests.post('http://localhost:5173/api/bybit/v2',data=req_json, headers={'Content-Type': 'application/json'})
        print(response)




def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()


[{'uid': '127397984', 
  'total_trade': 0.0, 
  'settled_commission': 0.0, 
  'date': '2023-12-26'},
   {'uid': '127299464', 'total_trade': 0.0, 'settled_commission': 0.0, 'date': '2023-12-26'},
   {'uid': '127243104', 'total_trade': 0.0, 'settled_commission': 0.0, 'date': '2023-12-26'},
   {'uid': '127240576', 'total_trade': 0.0, 'settled_commission': 0.0, 'date': '2023-12-26'},
   {'uid': '126054809', 'total_trade': 77925.67584066, 'settled_commission': 4.79392883, 'date': '2023-12-26'},
   {'uid': '125910226', 'total_trade': 0.0, 'settled_commission': 0.0, 'date': '2023-12-26'},
   {'uid': '125867683', 'total_trade': 0.0, 'settled_commission': 0.0, 'date': '2023-12-26'},
   {'uid': '122574037', 'total_trade': 0.0, 'settled_commission': 0.0, 'date': '2023-12-26'},
   {'uid': '121501598', 'total_trade': 1053998.082652, 'settled_commission': 121.09016389, 'date': '2023-12-26'},
   {'uid': '121313745', 'total_trade': 0.0, 'settled_commission': 0.0, 'date': '2023-12-26'},
   {'uid': '105413143', 'total_trade': 47290.37886, 'settled_commission': 7.41637698, 'date': '2023-12-26'},
   {'uid': '119947512', 'total_trade': 2341341.18893, 'settled_commission': 331.4818987, 'date': '2023-12-26'},
   {'uid': '112496341', 'total_trade': 0.0, 'settled_commission': 0.0, 'date': '2023-12-26'},
   {'uid': '111357071', 'total_trade': 0.0, 'settled_commission': 0.0, 'date': '2023-12-26'},
   {'uid': '110165455', 'total_trade': 0.0, 'settled_commission': 0.0, 'date': '2023-12-26'},
   {'uid': '110156005', 'total_trade': 0.0, 'settled_commission': 0.0, 'date': '2023-12-26'},
   {'uid': '110099988', 'total_trade': 0.0, 'settled_commission': 0.083495, 'date': '2023-12-26'},
   {'uid': '107964034', 'total_trade': 0.0, 'settled_commission': 0.0, 'date': '2023-12-26'},
   {'uid': '107655523', 'total_trade': 0.0, 'settled_commission': 0.0, 'date': '2023-12-26'},
   {'uid': '105600982', 'total_trade': 0.0, 'settled_commission': 0.0, 'date': '2023-12-26'}]