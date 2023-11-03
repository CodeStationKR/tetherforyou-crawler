import json
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from modules.base_crawler import BaseCrawler
import datetime

# 현재 로그인 안되고 있음

class BinanceCrawler(BaseCrawler):
    def __init__(self, chrome_path, user_data_directory, profile_directory):
        self.base_url = f"https://www.binance.com/en/activity/referral?stopRedirectToActivity=true"

        super().__init__(chrome_path, user_data_directory, profile_directory)

    def check_login_required(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'div#Commissions')
            return False
        except:
            return True
    
    def get_table_trs(self):
        table = self.driver.find_element(By.CSS_SELECTOR, 'div#Commissions div.bn-table-content > table')
        tbody = table.find_element(By.CSS_SELECTOR, 'tbody')
        trs = tbody.find_elements(By.CSS_SELECTOR, 'tr')
        return trs[1:]
    
    def preprocess(self, total_trade: str):
        total_trade = re.sub('[^0-9.]', '', total_trade)
        if(total_trade == ''):
            total_trade = 0.0
        total_trade = float(total_trade)
        return total_trade
    
    def can_go_next_page(self):
        try:
            next_page = self.driver.find_element(By.CSS_SELECTOR, 'div#Commissions button#next-page')
            return (not next_page.get_attribute('disabled'), next_page)
        except:
            return (False, None)
        
    def go_to_page(self, page):
        page_input = self.driver.find_element(By.CSS_SELECTOR, 'div.ant-pagination-options-quick-jumper > input')
        page_input.clear()
        page_input.send_keys(page)
        page_input.send_keys(Keys.ENTER)
        
    
    def get_uid(self, tds):
        return tds[1].text.replace('\n', '').replace(' ', '')

    def get_total_trade(self, tds):
        result = 0.0
        return result
    
    def get_commission_time(self, tds):
        text = tds[-2].text
        date = text.split(' ')[0]
        return datetime.datetime.strptime(date, '%Y-%m-%d').timestamp()
    
    def get_settled_commission(self, tds):
        result = 0.0
        settled_commission = tds[2].text
        if('\n' in settled_commission):
            settled_commissions = settled_commission.split('\n')
            for settled_commission in settled_commissions:
                settled_commission = self.preprocess(settled_commission)
                result += settled_commission
        else:
            result = self.preprocess(settled_commission)
        return result
    
    def get_result(self):
        trs = self.get_table_trs()
        for tr in trs:
            tds = tr.find_elements(By.CSS_SELECTOR, 'td')
            uid = self.get_uid(tds)
            total_trade = self.get_total_trade(tds)
            settled_commission = self.get_settled_commission(tds)
            commission_time = self.get_commission_time(tds)
            week_ago = datetime.datetime.now().timestamp() - 1 * 24 * 60 * 60
            if(commission_time < week_ago):
                return False
            self.upload(uid, total_trade, settled_commission)
            print('uid : ', uid, 'total : ',total_trade, 'settled : ',settled_commission , 'commission_time : ', commission_time,week_ago, 'should upload : ', commission_time > week_ago)
    
    def upload(self, uid, total_trade, settled_commission):
        url = self.base_api_url + '/binance'
        data = {
            'uid': uid,
            'transaction': total_trade,
            'payback': settled_commission * 0.9,
        }
        request_json = json.dumps(data)
        response = requests.post(url, data=request_json, headers={'Content-Type': 'application/json'})
        print(response.text)

    def run(self):
        print('Binance 크롤링을 시작합니다.')
        self.get(self.base_url)
        self.sleep(2)
        while self.check_login_required():
            input('로그인 후 엔터를 눌러주세요')
        self.get(self.base_url)
        self.sleep(2)
        while(self.can_go_next_page()[0]):
            result = self.get_result()
            if(result == False):
                break
            self.can_go_next_page()[1].click()
            self.sleep(2)
        self.driver.quit()
        print('Binance 크롤링을 종료합니다.')