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

def get_config():
    config_file = open('config.txt', 'r')
    config = {}
    for line in config_file.readlines():
        key, value = line.split('=')
        config[key] = value.replace('\n', '')
        config[key] = value.replace('\r', '')
        config[key] = value.replace('\t', '')
        # config[key] = value.replace(' ', '')
        config[key] = value.replace('\'', '')
    return config

def main():
    print(banner_text)
    config = get_config()
    # chrome_path = rf"{config['chrome_path']}"
    # user_data_directory = config['user_data_directory']
    # profile_directory = config['profile_directory']
    chrome_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    user_data_directory='/Users/kimminsu/Library/Application Support/Google/Chrome'
    profile_directory='Default'
    # bitget_crawler = BitgetCrawler(chrome_path, user_data_directory, profile_directory)
    # bitget_crawler.run()
    # bybit_crawler = BybitCrawler(chrome_path, user_data_directory, profile_directory)
    # bybit_crawler.run()
    # okx_crawler = OkxCrawler(chrome_path, user_data_directory, profile_directory)
    # okx_crawler.run()
    bitmart_crawler = BitmartCrawler(chrome_path, user_data_directory, profile_directory)
    bitmart_crawler.run()

if __name__ == '__main__':
    main()