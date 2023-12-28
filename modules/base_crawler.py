import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class BaseCrawler():
    def __init__(self, chrome_path, user_data_directory, profile_directory):
        self.base_api_url = 'https://tetherforyou.com/api'
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36')
        # for pc version
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Safari/537.36')
        # add user profile
        options.add_argument(f"user-data-dir={user_data_directory}")
        options.add_argument(f"profile-directory={profile_directory}")

        options.binary_location = chrome_path
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

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