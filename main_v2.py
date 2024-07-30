from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from v2.modules.binance_crawler import BinanceCrawler
from v2.modules.bingx_crawler import BingXCrawler
from v2.modules.bitget_crawler import BitgetCrawler
from v2.modules.bitmart_crawler import BitmartCrawler
from v2.modules.bybit_crawler import BybitCrawler
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

banner_text = '''
___________     __  .__                ___________          _____.___.             
\__    ___/____/  |_|  |__   __________\_   _____/__________\__  |   | ____  __ __ 
  |    |_/ __ \   __\  |  \_/ __ \_  __ \    __)/  _ \_  __ \/   |   |/  _ \|  |  \\
  |    |\  ___/|  | |   Y  \  ___/|  | \/     \(  <_> )  | \/\____   (  <_> )  |  /
  |____| \___  >__| |___|  /\___  >__|  \___  / \____/|__|   / ______|\____/|____/ 
             \/          \/     \/          \/               \/                    
'''

def main():
    print(banner_text)
 
    # chrome_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    # user_data_directory='C:\\Users\\metas\\AppData\\Local\\Google\\Chrome\\User Data'
    # profile_directory='Profile 1'

    chrome_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    user_data_directory='C:\\Users\\metas\\AppData\\Local\\Google\\Chrome\\User Data'
    profile_directory='Profile 1'

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-extensions')
    options.add_argument('--dns-prefetch-disable')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument('--disable-infobars')

    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")

    # disable the banner "Chrome is being controlled by automated test software"
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ['enable-automation'])

    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Safari/537.36')
    # add user profile
    options.add_argument(f"--user-data-dir={user_data_directory}")
    options.add_argument(f"--profile-directory={profile_directory}")

    options.binary_location = chrome_path
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver = webdriver.Chrome(options=options)

    try:
        bingx_crawler = BingXCrawler(driver)
        bingx_crawler.run()
    except Exception as e:
        print('빙엑스 크롤링 중 에러 발생')
        print(e)
    
    try:
        bybit_crawler = BybitCrawler(driver)
        bybit_crawler.run()
    except Exception as e:
        print('바이비트 크롤링 중 에러 발생')
        print(e)

    try:
        bitmart_crawler = BitmartCrawler(driver)
        bitmart_crawler.run()
    except Exception as e:
        print('비트마트 크롤링 중 에러 발생')
        print(e)

    try:
        binance_crawler = BinanceCrawler(driver)
        binance_crawler.run()
    except Exception as e:
        print('바이낸스 크롤링 중 에러 발생')
        print(e)

    try:
        bitget_crawler = BitgetCrawler(driver)
        bitget_crawler.run()
    except Exception as e:

        print('비트겟 크롤링 중 에러 발생')
        print(e)

    input('Press any key to continue...')
    driver.quit()
        

if __name__ == '__main__':
    main()

