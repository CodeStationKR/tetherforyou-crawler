from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bybit_crawler import BybitCrawlerV2

from modules.bybit_crawler import BybitCrawler

AUTH = 'brd-customer-hl_25a514e6-zone-scraping_browser:y3wtd8t81wx6'
SBR_WEBDRIVER = f'https://{AUTH}@zproxy.lum-superproxy.io:9515'

def main():
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        bybit_crawler = BybitCrawlerV2(driver=driver)
        bybit_crawler.run()

if __name__ == '__main__':
    main()
