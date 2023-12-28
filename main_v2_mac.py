from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from v2.modules.binance_crawler import BinanceCrawler
from v2.modules.bingx_crawler import BingXCrawler
from v2.modules.bitget_crawler import BitgetCrawler
from v2.modules.bitmart_crawler import BitmartCrawler
from v2.modules.bybit_crawler import BybitCrawler
from v2.modules.okx_crawler import OkxCrawler
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
 
    chrome_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    user_data_directory='/Users/kimminsu/Library/Application Support/Google/Chrome'
    profile_directory='Profile 3'
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36')
    # add user profile
    options.add_argument(f"user-data-dir={user_data_directory}")
    options.add_argument(f"profile-directory={profile_directory}")

    options.binary_location = chrome_path
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # try:
    #     binance_crawler = BinanceCrawler(chrome_path, user_data_directory, profile_directory)
    #     binance_crawler.run()
    # except Exception as e:
    #     print('바이낸스 크롤링 중 에러 발생')
    #     print(e)

    # try:
    #     bingx_crawler = BingXCrawler(chrome_path, user_data_directory, profile_directory)
    #     bingx_crawler.run()
    # except Exception as e:
    #     print('빙엑스 크롤링 중 에러 발생')
    #     print(e)
    
    try:
        bybit_crawler = BybitCrawler(driver)
        bybit_crawler.run()
    except Exception as e:
        print('바이비트 크롤링 중 에러 발생')
        print(e)

    # try:
    #     okx_crawler = OkxCrawler(chrome_path, user_data_directory, profile_directory)
    #     okx_crawler.run()
    # except Exception as e:
    #     print('OKX 크롤링 중 에러 발생')
    #     print(e)

    # try:
    #     bitmart_crawler = BitmartCrawler(chrome_path, user_data_directory, profile_directory)
    #     bitmart_crawler.run()
    # except Exception as e:
    #     print('비트마트 크롤링 중 에러 발생')
    #     print(e)

    # try:
    #     bitget_crawler = BitgetCrawler(chrome_path, user_data_directory, profile_directory)
    #     bitget_crawler.run()
    # except Exception as e:

    #     print('비트겟 크롤링 중 에러 발생')
       
    #     print(e)
    driver.quit()
        

if __name__ == '__main__':
    main()

