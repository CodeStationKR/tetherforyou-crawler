from modules.binance_crawler import BinanceCrawler
from modules.bingx_crawler import BingXCrawler
from modules.bitget_crawler import BitgetCrawler
from modules.bitmart_crawler import BitmartCrawler
from modules.bybit_crawler import BybitCrawler
from modules.okx_crawler import OkxCrawler

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
    # tetherforyou 733
    chrome_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    user_data_directory='C:\\Users\\pc\\AppData\\Local\\Google\\Chrome\\User Data'
    profile_directory='Profile 733'
    try:
        binance_crawler = BinanceCrawler(chrome_path, user_data_directory, profile_directory)
        binance_crawler.run()
    except Exception as e:
        print('바이낸스 크롤링 중 에러 발생')
        print(e)

    try:
        bingx_crawler = BingXCrawler(chrome_path, user_data_directory, profile_directory)
        bingx_crawler.run()
    except Exception as e:
        print('빙엑스 크롤링 중 에러 발생')
        print(e)
    
    try:
        bybit_crawler = BybitCrawler(chrome_path, user_data_directory, profile_directory)
        bybit_crawler.run()
    except Exception as e:
        print('바이비트 크롤링 중 에러 발생')
        print(e)

    try:
        okx_crawler = OkxCrawler(chrome_path, user_data_directory, profile_directory)
        okx_crawler.run()
    except Exception as e:
        print('OKX 크롤링 중 에러 발생')
        print(e)

    try:
        bitmart_crawler = BitmartCrawler(chrome_path, user_data_directory, profile_directory)
        bitmart_crawler.run()
    except Exception as e:
        print('비트마트 크롤링 중 에러 발생')
        print(e)

    try:
        bitget_crawler = BitgetCrawler(chrome_path, user_data_directory, profile_directory)
        bitget_crawler.run()
    except Exception as e:

        print('비트겟 크롤링 중 에러 발생')
       
        print(e)

if __name__ == '__main__':
    main()