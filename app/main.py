from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

email = 'marineteamkr@naver.com'
password = 'Metasplo1t!23'

chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36')
options.binary_location = chrome_path
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver = webdriver.Chrome(options=options)

today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
yesterday = time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400))

base_url = f"https://affiliates.bybit.com/v2/affiliate-portal/clients?offset=0&coin=All&uid=&page_size=20&start_date={yesterday}&end_date={today}&business=0"
driver.get(base_url)

email_input = driver.find_element(By.CSS_SELECTOR, 'input#login_email')
email_input.send_keys(email)

password_input = driver.find_element(By.CSS_SELECTOR, 'input#login_password')
password_input.send_keys(password)

login_button = driver.find_element(By.CSS_SELECTOR, 'button.login-btn')
login_button.click()
input('Press Enter to continue')
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
    total_trade = float(total_trade)

    settled_commission = tds[-1].text
    settled_commission = settled_commission.replace(' USDT', '')
    settled_commission = settled_commission.replace(',', '')
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
        total_trade = float(total_trade)

        settled_commission = tds[-1].text
        settled_commission = settled_commission.replace(' USDT', '')
        settled_commission = settled_commission.replace(',', '')
        settled_commission = float(settled_commission)

        print('uid : ', uid, 'total : ',total_trade, 'settled : ',settled_commission)
input("Press Enter to quit")