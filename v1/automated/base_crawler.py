import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class BaseCrawlerV2():
    def __init__(self, driver):
        self.base_api_url = 'https://tetherforyou.com/api'
        self.driver = driver
        

    def get(self, url):
        # get url and wait for only 5 seconds
        
        self.driver.get(url)
        

    def check_login_required(self):
        return True
    
    def login(self, email, password):
        pass

    def go_to_page(self, page):
        pass

    def get_total_pages(self):
        pass

    def get_result(self):
        pass

    def sleep(self, seconds):
        time.sleep(seconds)

    def run(self):
        input('Press any key to continue...')