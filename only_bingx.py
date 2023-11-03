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
  
    bingx_crawler = BingXCrawler(chrome_path, user_data_directory, profile_directory)
    bingx_crawler.run()
 

if __name__ == '__main__':
    main()