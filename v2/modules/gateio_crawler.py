import json
import pickle
import time
import requests
from v2.modules.base_crawler import BaseCrawler
import re
from selenium.webdriver.common.by import By
from selenium import webdriver


class GateIoCrawler(BaseCrawler):

    def __init__(self, driver : webdriver.Chrome):        
        self.base_url = f"https://www.gate.io/partner/admin/customerManagement/customer"
        super().__init__(driver)

    def check_login_required(self):
        return 'https://www.gate.io/referral' == self.driver.current_url
    
    def check_has_next_page(self):
        next_page = self.driver.find_element(By.CSS_SELECTOR, 'li.ant-pagination-next')
        return 'ant-pagination-disabled' not in next_page.get_attribute('class')
    
    def go_to_next_page(self):
        next_page = self.driver.find_element(By.CSS_SELECTOR, 'li.ant-pagination-next')
        next_page.click()
        time.sleep(5)
    
    def get_table_trs(self):
        table = self.driver.find_element(By.CSS_SELECTOR, 'div.ant-table-content table')
        tbody = table.find_element(By.CSS_SELECTOR, 'tbody')
        trs = tbody.find_elements(By.CSS_SELECTOR, 'tr')
        trs = trs[1:]
        return trs
    
    def preprocess(self, total_trade: str):
        total_trade = re.sub('[^0-9.]', '', total_trade)
        if(total_trade == ''):
            total_trade = 0.0
        total_trade = float(total_trade)
        return total_trade
    
    def get_uid(self, tds):
        uid = tds[0].text
        uid = uid.replace('\n', '')
        uid = uid.replace(' ', '')
        return uid
    
    def get_total_trade(self, tds):
        # daily transaction fee
        result = 0.0
        total_trade = tds[-5].text
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
        settled_commission = tds[-4].text
        if('\n' in settled_commission):
            settled_commissions = settled_commission.split('\n')
            for settled_commission in settled_commissions:
                settled_commission = self.preprocess(settled_commission)
                result += settled_commission
        else:
            result = self.preprocess(settled_commission)
        return result
    
    def upload(self, results: list[dict]):
        self.base_api_url = 'http://localhost:5173/api'
        url = self.base_api_url + '/gate-io/v2'
        data = {
            'reqs': results
        }
        request_json = json.dumps(data)
        response = requests.post(url, data=request_json, headers={'Content-Type': 'application/json'})
        print(response.text)
    
    def get_results(self):
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        results = []
        trs = self.get_table_trs()
        for tr in trs:
            tds = tr.find_elements(By.CSS_SELECTOR, 'td')

            uid = self.get_uid(tds)
            total_trade = self.get_total_trade(tds)
            settled_commission = self.get_settled_commission(tds)
            print(settled_commission, 'payback', settled_commission * 0.9)
            results.append({
                'uid': uid,
                'transaction': total_trade,
                'payback': settled_commission * 0.9,
                'date': today,
            })
        return results


    def run(self):
        print('Gate.io 크롤링을 시작합니다.')
        self.get(self.base_url)

        self.sleep(2)

        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            print(cookies)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        except Exception as e:
            print(e)
            print('쿠키 파일을 찾을 수 없습니다.')
        while self.check_login_required():
            input('로그인 후 엔터를 눌러주세요')
        self.get(self.base_url)

        self.sleep(2)
        while self.check_has_next_page():
            results = self.get_results()
            print(results)
            print('페이지 크롤링 완료, 업로드를 시작합니다.')
            self.upload(results)
            self.go_to_next_page()
            self.sleep(2)
        results = self.get_results()
        print(results)
        print('페이지 크롤링 완료, 업로드를 시작합니다.')
        
        self.upload(results)
        input('엔터를 눌러주세요')

        print('Gate.io 크롤링을 종료합니다.')
        
