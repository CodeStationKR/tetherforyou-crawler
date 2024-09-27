import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class BaseCrawler():
    def __init__(self, driver : webdriver.Chrome):
        self.base_api_url = 'https://tetherforyou-com.vercel.app/api'
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

    def get_results(self):
        pass

    def sleep(self, seconds):
        time.sleep(seconds)

    def run(self):
        input('Press any key to continue...')