import json
import re
import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from v2.modules.base_crawler import BaseCrawler
from selenium import webdriver


class BitgetCrawler(BaseCrawler):

    def __init__(self, driver : webdriver.Chrome):        
        self.base_url = f"https://newaffiliates.bitget.com/user-manage/user-business"
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
        if(total_trade == ''):
            total_trade = 0.0
        total_trade = float(total_trade)
        if(total_trade < 0):
            total_trade = -total_trade
        return total_trade
    
    def get_total_pages(self):
        total_count = self.driver.find_element(By.CSS_SELECTOR, 'ul.ant-pagination li.ant-pagination-total-text').text
        total_count = re.sub('[^0-9]', '', total_count)
        total_count = int(total_count)
        # a page has 10 items
        # if 10 items are in a page, total pages should be 1
        # if 11 items are in a page, total pages should be 2
        # 11 // 10 = 1 (this is the case of 11 items in a page, so total pages should be 2)
        # 10 // 10 = 1
        total_pages = int(total_count / 10)
        if(total_count % 10 != 0):
            total_pages += 1
        return total_pages

        
    def go_to_page(self, page):
        page_input = self.driver.find_element(By.CSS_SELECTOR, 'div.ant-pagination-options-quick-jumper > input')
        page_input.clear()
        page_input.send_keys(page)
        page_input.send_keys(Keys.ENTER)

    def go_to_date(self, day):
        start_date_input = self.driver.find_elements(By.CSS_SELECTOR, 'div.ant-picker-input input')[0]
        backspace = Keys.BACKSPACE
        for _ in range(10):
            start_date_input.send_keys(backspace)
       
        start_date_input.send_keys(day)

        end_date_input = self.driver.find_elements(By.CSS_SELECTOR, 'div.ant-picker-input input')[1]
        for _ in range(10):
            end_date_input.send_keys(backspace)
        end_date_input.send_keys(day)
        end_date_input.send_keys(Keys.ENTER)

        inquire_button = self.driver.find_elements(By.CSS_SELECTOR, 'div.ant-form-item-control-input-content > button')[1]
        inquire_button.click()

        
    def get_uid(self, tds):
        return tds[1].text.replace('\n', '').replace(' ', '')

    def get_total_trade(self, tds):
        result = 0.0
        total_trade = tds[4].find_element(By.CSS_SELECTOR, 'div > span').text
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
        settled_commission = tds[-6].find_element(By.CSS_SELECTOR, 'div > span').text
        if('\n' in settled_commission):
            settled_commissions = settled_commission.split('\n')
            for settled_commission in settled_commissions:
                settled_commission = self.preprocess(settled_commission)
                result += settled_commission
        else:
            result = self.preprocess(settled_commission)
        
        return result
    
    def get_results(self, day):
        results = []
        trs = self.get_table_trs()
        for tr in trs:
            tds = tr.find_elements(By.CSS_SELECTOR, 'td')
            uid = self.get_uid(tds)
            total_trade = self.get_total_trade(tds)
            settled_commission = self.get_settled_commission(tds)
            print(uid, total_trade, settled_commission)
            results.append({
                'uid': uid,
                'transaction': total_trade,
                'payback': settled_commission * 0.9,
                'date': day
            })
        return results
    # 2331976346
    
    def close_modal(self):
        close_button = self.driver.find_element(By.CSS_SELECTOR, 'div.ant-modal-content > button.ant-modal-close')
        close_button.click()
            
    
    def upload(self, results: list[dict]):
        # self.base_api_url = 'http://localhost:5173/api'

        url = self.base_api_url + '/bitget/v2'
        data = {
            'reqs': results
        }
        request_json = json.dumps(data)
        response = requests.post(url, data=request_json, headers={'Content-Type': 'application/json'})
        print(response.text)

    def run(self):
        print('Bitget 크롤링을 시작합니다.')
        six_days_ago = time.strftime('%Y-%m-%d', time.localtime(time.time() - 60 * 60 * 24 * 6))
        five_days_ago = time.strftime('%Y-%m-%d', time.localtime(time.time() - 60 * 60 * 24 * 5))
        four_days_ago = time.strftime('%Y-%m-%d', time.localtime(time.time() - 60 * 60 * 24 * 4))
        three_days_ago = time.strftime('%Y-%m-%d', time.localtime(time.time() - 60 * 60 * 24 * 3))
        two_days_ago = time.strftime('%Y-%m-%d', time.localtime(time.time() - 60 * 60 * 24 * 2))
        yesterday = time.strftime('%Y-%m-%d', time.localtime(time.time() - 60 * 60 * 24))
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        days = [
            six_days_ago,
five_days_ago,
four_days_ago,
            three_days_ago,
            two_days_ago,   
            yesterday,
            today
        ]
        self.get(self.base_url)
        self.sleep(2)
        while self.check_login_required():
            input('로그인 후 엔터를 눌러주세요')
        for day in days:
            
            self.get(self.base_url)
            self.sleep(3)
            try:
                self.close_modal()
            except:
                pass
            self.sleep(1)
            self.go_to_date(day)
            self.sleep(2)
            self.go_to_date(day)
            self.sleep(2)
            try:
                total_pages = self.get_total_pages()
                total_pages = int(input(f'받아온 토탈 페이지 수는 {total_pages}입니다. 확인차 페이지 수를 입력해주세요 : '))
            except: 
                total_pages = int(input('페이지 수를 읽어오는데 실패했습니다. 페이지 수를 입력해주세요 : '))
            for page in range(1, total_pages + 1):
                if(page > 1):
                    self.go_to_page(page)
                print(f'{day} {page} 페이지 크롤링 중... {total_pages} 페이지 중 {page} 페이지')
                self.sleep(2)
                results = self.get_results(day)
                print(results)
                print(f'{day} {page} 페이지 크롤링 완료')
                print('업로드를 시작합니다.')
                self.upload(results)
        print('Bitget 크롤링을 종료합니다.')

