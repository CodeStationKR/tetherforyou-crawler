import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36')
# add user profile
options.add_argument("user-data-dir=Chrome")
options.add_argument("profile-directory=Default")

options.binary_location = chrome_path
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver = webdriver.Chrome(options=options)

today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
yesterday = time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400))

base_url = f"https://affiliates.bybit.com/v2/affiliate-portal/clients?offset=0&coin=All&uid=&page_size=20&start_date={yesterday}&end_date={today}&business=0"
driver.get(base_url)
input()
results_h5 = driver.find_elements(By.CSS_SELECTOR, 'div.clients-page-table-panel > h5.ant-typography')[0].text.replace(' Results', '')
results = int(results_h5)
print(results)
total_page = results // 20 + 1
print(total_page)
table = driver.find_element(By.CSS_SELECTOR, 'div.ant-table-content > table')
tbody = table.find_element(By.CSS_SELECTOR, 'tbody')
trs = tbody.find_elements(By.CSS_SELECTOR, 'tr')
print('page : 1')
for tr in trs[1:]:
    tds = tr.find_elements(By.CSS_SELECTOR, 'td')
    uid = tds[0].text
    total_trade = tds[6].text
    total_trade = total_trade.replace(' USDT', '')
    total_trade = total_trade.replace(',', '')
    total_trade = re.sub('[^0-9.]', '', total_trade)

    total_trade = float(total_trade)

    settled_commission = tds[-1].text
    settled_commission = settled_commission.replace(' USDT', '')
    settled_commission = settled_commission.replace(',', '')
    settled_commission = re.sub('[^0-9.]', '', settled_commission)
    settled_commission = float(settled_commission)

    print('uid : ', uid, 'total : ',total_trade, 'settled : ',settled_commission)
for page in range(2, total_page + 1):
    print('page : ', page)
    url = base_url + f'&page={page}'
    driver.get(url)
    time.sleep(3)
    table = driver.find_element(By.CSS_SELECTOR, 'div.ant-table-content > table')
    tbody = table.find_element(By.CSS_SELECTOR, 'tbody')
    trs = tbody.find_elements(By.CSS_SELECTOR, 'tr')
    for tr in trs[1:]:
        tds = tr.find_elements(By.CSS_SELECTOR, 'td')
        uid = tds[0].text
        total_trade = tds[6].text
        total_trade = total_trade.replace(' USDT', '')
        total_trade = total_trade.replace(',', '')
        # remove all except numbers and dot
        total_trade = re.sub('[^0-9.]', '', total_trade)
        total_trade = float(total_trade)

        settled_commission = tds[-1].text
        settled_commission = settled_commission.replace(' USDT', '')
        settled_commission = settled_commission.replace(',', '')
        settled_commission = re.sub('[^0-9.]', '', settled_commission)

        settled_commission = float(settled_commission)

        print('uid : ', uid, 'total : ',total_trade, 'settled : ',settled_commission)
input("Press Enter to quit")