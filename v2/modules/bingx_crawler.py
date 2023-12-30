import json
import re
import time
import requests
from selenium.webdriver.common.by import By
from v2.modules.base_crawler import BaseCrawler
from selenium import webdriver
# import Keys
from selenium.webdriver.common.keys import Keys


class BingXCrawler(BaseCrawler):
    def __init__(self, driver : webdriver.Chrome):        
        self.base_url = f"https://hi.bingx.com/commission/userDetail"
        super().__init__(driver)

    def check_login_required(self):
        return 'login' in self.driver.current_url
    
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
        uid= tds[0].text.split('\n')[0].replace('\n', '').replace(' ', '')
        uid = re.sub('[^0-9.]', '', uid)
        return uid

    def get_total_trade(self, tds):
        result = 0.0
        total_trade = tds[3].text
        if('\n' in total_trade):
            total_trades = total_trade.split('\n')
            for total_trade in total_trades:
                total_trade = self.preprocess(total_trade)
                result += total_trade
        else:
            result = self.preprocess(total_trade)
        return result
    
    def upload(self, results: list[dict]):
        # self.base_api_url = 'http://localhost:5173/api'
        url = self.base_api_url + '/bingx/v2'
        data = {
            'reqs': results
        }
        request_json = json.dumps(data)
        response = requests.post(url, data=request_json, headers={'Content-Type': 'application/json'})
        print(response.text)
    
    def get_settled_commission(self, tds):
        result = 0.0
        settled_commission = tds[-3].text
        if('\n' in settled_commission):
            settled_commissions = settled_commission.split('\n')
            for settled_commission in settled_commissions:
                settled_commission = self.preprocess(settled_commission)
                result += settled_commission
        else:
            result = self.preprocess(settled_commission)
        return result
    
    def get_results(self, day):
        trs = self.get_table_trs()
        results = []
        for tr in trs:
            tds = tr.find_elements(By.CSS_SELECTOR, 'td')
            uid = self.get_uid(tds)
            total_trade = self.get_total_trade(tds)
            settled_commission = self.get_settled_commission(tds)
            results.append({
                'uid': uid,
                'transaction': total_trade,
                'payback': settled_commission * 0.9,
                'date': day
            })
        return results

    def go_to_page(self, day):
        date = day.replace('-', '/')
        start_time_input = self.driver.find_elements(By.CSS_SELECTOR, 'div.ant-picker-input > input')[0]
       
        backspace = Keys.BACKSPACE
        for _ in range(10):
            start_time_input.send_keys(backspace)
        start_time_input.send_keys(date)

        end_time_input = self.driver.find_elements(By.CSS_SELECTOR, 'div.ant-picker-input > input')[1]
        
        for _ in range(10):
            end_time_input.send_keys(backspace)
        end_time_input.send_keys(date)
        end_time_input.send_keys(Keys.ENTER)

        search_button = self.driver.find_element(By.CSS_SELECTOR, 'button.ant-btn.ant-btn-primary.btn-search')
        search_button.click()

        self.sleep(2)

    def run(self):
        print('BingX 크롤링을 시작합니다.')
        self.get(self.base_url)
        self.sleep(2)

        two_days_ago = time.strftime('%Y-%m-%d', time.gmtime(time.time() - 60 * 60 * 24 * 2))
        yesterday = time.strftime('%Y-%m-%d', time.gmtime(time.time() - 60 * 60 * 24))
        today = time.strftime('%Y-%m-%d', time.gmtime(time.time()))

        days = [
            two_days_ago,   
            yesterday,
            today
        ]

        while self.check_login_required():
            input('로그인 후 엔터를 눌러주세요')
        self.get(self.base_url)
        self.sleep(2)
        for day in days:
            self.go_to_page(day)
            print(f'{day} 데이터 업로드 중...')
            results = self.get_results(day)
            self.upload(results)
            print(f'{day} 데이터 업로드 완료')

        input('엔터를 눌러주세요')
        print('BingX 크롤링을 종료합니다.')

