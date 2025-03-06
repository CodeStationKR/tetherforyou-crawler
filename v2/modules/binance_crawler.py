import json
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from v2.modules.base_crawler import BaseCrawler
import datetime
from selenium import webdriver

class BinanceCrawler(BaseCrawler):
    def __init__(self, driver : webdriver.Chrome):
        self.results = {} 
        self.base_url = f"https://www.binance.com/en/activity/referral?stopRedirectToActivity=true"
        super().__init__(driver)
  

    def check_login_required(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'div.bn-flex > div.bn-tabs > div.bn-tab-list > div')
            return False
        except:
            return True
    
    def get_table_trs(self):
        self.click_reward()
        self.sleep(2)
        table = self.driver.find_element(By.CSS_SELECTOR, 'div.bn-web-table-content > table')
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
            pages = self.driver.find_elements(By.CSS_SELECTOR, 'div.bn-pagination-items > a')
            currentPage = 0
            for i, page in enumerate(pages):
                if 'active' not in page.get_attribute('class'):
                    continue
                if len(pages) - 1 == i:
                    return (False, None) # last page
                text = page.text
                currentPage = int(text)
            for page in pages:
                text = page.text
                nextPageText = str(currentPage + 1)
                if text == nextPageText:
                    return (True, page)
        except Exception as e:
            print(e)
            return (False, None)

    def click_reward(self): 
        reward_btns = self.driver.find_elements(By.CSS_SELECTOR, "div.bn-flex > div.bn-tabs > div.bn-tab-list > div")
        reward_btn = reward_btns[1]
        try:
            reward_btn.click()
        except:
            pass
        
    
    def get_uid(self, tds):
        return tds[0].text.replace('\n', '').replace(' ', '')

    def get_total_trade(self, tds):
        result = 1
        return result
    
    def get_commission_time(self, tds):
        text = tds[2].text
        date = text.split(' ')[0]
        return datetime.datetime.strptime(date, '%Y-%m-%d')
    
    def get_settled_commission(self, tds):
        result = 0.0
        settled_commission = tds[-2].text
        if('USDT' not in settled_commission):
            return result
        if('\n' in settled_commission):
            settled_commissions = settled_commission.split('\n')
            for settled_commission in settled_commissions:
                settled_commission = self.preprocess(settled_commission)
                result += settled_commission
        else:
            result = self.preprocess(settled_commission)
        return result
    
    def get_results(self):
        trs = self.get_table_trs()
     
        for tr in trs:
            tds = tr.find_elements(By.CSS_SELECTOR, 'td')
            uid = self.get_uid(tds)
            total_trade = self.get_total_trade(tds)
            settled_commission = self.get_settled_commission(tds)
            commission_time = self.get_commission_time(tds)
            commission_time_str = commission_time.strftime('%Y-%m-%d')
            
            result = {
                'uid': uid,
                'transaction': total_trade,
                'payback': settled_commission * 0.9,
                'date': commission_time_str,
            }
            print(result)

            today = datetime.datetime.now()
            today = datetime.datetime(today.year, today.month, today.day)
            two_days_ago = today - datetime.timedelta(days=5)
            if(commission_time < two_days_ago):
                return False

            if commission_time_str not in self.results:
                self.results[commission_time_str] = {}
            if uid not in self.results[commission_time_str]:
                self.results[commission_time_str][uid] = result
            else:
                self.results[commission_time_str][uid]['payback'] += result['payback']
    
    def preprocess_results(self):
        results = []
        for date in self.results.keys():
            for uid in self.results[date].keys():
                results.append(self.results[date][uid])
        return results
    
    def upload(self, results: list[dict]):
        # self.base_api_url = 'http://localhost:5173/api'
        url = self.base_api_url + '/binance/v2'
        data = {
            'reqs': results
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


        try:
            while(self.can_go_next_page()[0]):
                result = self.get_results()
                if(result == False):
                    break
                self.can_go_next_page()[1].click()
                self.sleep(5)
        except Exception as e:
            self.get(self.base_url)
            self.sleep(2)
            while(self.can_go_next_page()[0]):
                result = self.get_results()
                if(result == False):
                    break
                self.can_go_next_page()[1].click()
                self.sleep(2)
        results = self.preprocess_results()
        print(results)
        print('페이지 크롤링 완료, 업로드를 시작합니다.')
        self.upload(results)
        print('Binance 크롤링을 종료합니다.')
       