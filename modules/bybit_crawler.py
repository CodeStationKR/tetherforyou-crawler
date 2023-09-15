import json
import re
import time
import requests
from selenium.webdriver.common.by import By
from modules.base_crawler import BaseCrawler

class BybitCrawler(BaseCrawler):
    def __init__(self, chrome_path, user_data_directory, profile_directory):
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self.base_url = f"https://affiliates.bybit.com/v2/affiliate-portal/clients?offset=0&coin=All&uid=&page_size=20&start_date={today}&end_date={today}&business=0"

        super().__init__(chrome_path, user_data_directory, profile_directory)

    def check_login_required(self):
        return 'login' in self.driver.current_url
    
    def get_total_pages(self):
        results_h5 = self.driver.find_elements(By.CSS_SELECTOR, 'div.clients-page-table-panel > h5.ant-typography')[0].text.replace(' Results', '')
        results = int(results_h5)
        total_page = results // 20 + 1
        return total_page
    
    def get_table_trs(self):
        table = self.driver.find_element(By.CSS_SELECTOR, 'div.ant-table-content > table')
        tbody = table.find_element(By.CSS_SELECTOR, 'tbody')
        trs = tbody.find_elements(By.CSS_SELECTOR, 'tr')
        return trs[1:]
    
    def preprocess(self, total_trade: str):
        total_trade = re.sub('[^0-9.]', '', total_trade)
        total_trade = float(total_trade)
        return total_trade
    
    def get_uid(self, tds):
        return tds[0].text.replace('\n', '').replace(' ', '')

    def get_total_trade(self, tds):
        result = 0.0
        total_trade = tds[-3].text
        if('\n' in total_trade):
            total_trades = total_trade.split('\n')
            for total_trade in total_trades:
                total_trade = self.preprocess(total_trade)
                result += total_trade
        else:
            result = self.preprocess(total_trade)
        return result
    
    def get_settled_commission(self, tds):
        result = 0.0
        settled_commission = tds[1].text
        if('\n' in settled_commission):
            settled_commissions = settled_commission.split('\n')
            for settled_commission in settled_commissions:
                settled_commission = self.preprocess(settled_commission)
                result += settled_commission
        else:
            result = self.preprocess(settled_commission)
        return result
    
    def go_to_page(self, page):
        url = self.base_url + f'&page={page}'
        self.get(url)

    def upload(self, uid, total_trade, settled_commission):
        url = self.base_api_url + '/bybit'
        data = {
            'uid': uid,
            'transaction': total_trade,
            'payback': settled_commission * 0.9,
        }
        request_json = json.dumps(data)
        response = requests.post(url, data=request_json, headers={'Content-Type': 'application/json'})
        print(response.text)
    
    def get_result(self):
        trs = self.get_table_trs()
        for tr in trs:
            tds = tr.find_elements(By.CSS_SELECTOR, 'td')
            uid = self.get_uid(tds)
            total_trade = self.get_total_trade(tds)
            settled_commission = self.get_settled_commission(tds)
            self.upload(uid, total_trade, settled_commission)
            print('uid : ', uid, 'total : ',total_trade, 'settled : ',settled_commission)

    def run(self):
        print('Bybit 크롤링을 시작합니다.')

        self.get(self.base_url)
        self.sleep(2)
        while self.check_login_required():
            input('로그인 후 엔터를 눌러주세요')
        self.sleep(2)

        total_page = self.get_total_pages()
        for i in range(1, total_page + 1):
            self.go_to_page(i)
            self.sleep(2)
            self.get_result()
        input('크롤링이 완료되었습니다. 엔터를 눌러주세요.')
        self.driver.quit()
        print('Bybit 크롤링을 종료합니다.')
