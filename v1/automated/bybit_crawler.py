import json
import re
import time
import requests
from selenium.webdriver.common.by import By
from base_crawler import BaseCrawlerV2

class BybitCrawlerV2(BaseCrawlerV2):
    def __init__(self, driver):        
        super().__init__(driver=driver)

    def get_base_url(self, start_date, end_date):
        return f'https://affiliates.bybit.com/v2/affiliate-portal/clients?offset=0&coin=All&uid=&page_size=20&start_date={start_date}&end_date={end_date}&business=0'
        

    def check_login_required(self):
        return 'login' in self.driver.current_url
    
    def login(self):
        self.sleep(5)
        email_input = self.driver.find_element(By.CSS_SELECTOR, 'input#login_email')
        password_input = self.driver.find_element(By.CSS_SELECTOR, 'input#login_password')
        email_input.send_keys('marineteamkr@naver.com')
        password_input.send_keys('Metasplo1t!23')
        self.sleep(2)
        login_button = self.driver.find_element(By.CSS_SELECTOR, 'button.ant-btn')
        login_button.click()
        self.sleep(5)
    
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
        if(total_trade == ''):
            total_trade = 0.0
        total_trade = float(total_trade)
        if(total_trade < 0):
            total_trade = -total_trade
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
            settled_commission = settled_commission.split('\n')[0]
            
        else:
            result = self.preprocess(settled_commission)
        return result
    
    def go_to_page(self, page, url):
        url = url + f'&page={page}'
        self.get(url)

    def upload(self, uid, total_trade, settled_commission, day):
        url = self.base_api_url + '/bybit'
        data = {
            'uid': uid,
            'transaction': total_trade,
            'payback': settled_commission * 0.9,
            'date': day
        }
        request_json = json.dumps(data)
        response = requests.post(url, data=request_json, headers={'Content-Type': 'application/json'})
        print(response.text)
    
    def get_result(self, day):
        trs = self.get_table_trs()
        for tr in trs:
            tds = tr.find_elements(By.CSS_SELECTOR, 'td')
            uid = self.get_uid(tds)
            total_trade = self.get_total_trade(tds)
            settled_commission = self.get_settled_commission(tds)
            self.upload(uid, total_trade, settled_commission, day)
            print('uid : ', uid, 'total : ',total_trade, 'settled : ',settled_commission)

    def run(self):
        print('Bybit 크롤링을 시작합니다.')
        two_days_ago = time.strftime('%Y-%m-%d', time.localtime(time.time() - 60 * 60 * 24 * 2))
        yesterday = time.strftime('%Y-%m-%d', time.localtime(time.time() - 60 * 60 * 24))
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        days = [
            two_days_ago,
            yesterday,
            today,
        ]

        for day in days:
            url = self.get_base_url(day, day)
            self.get(url)
            self.sleep(2)
            while self.check_login_required():
                self.login()
                self.get(url)
            self.sleep(2)

            total_page = self.get_total_pages()
            for i in range(1, total_page + 1):
                self.go_to_page(i, url)
                self.sleep(2)
                self.get_result(day)
        input('크롤링이 완료되었습니다. 엔터를 눌러주세요.')
        self.driver.quit()
        print('Bybit 크롤링을 종료합니다.')
