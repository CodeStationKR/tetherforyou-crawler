import pickle
import undetected_chromedriver as uc
from selenium_stealth import stealth
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from v2.modules.gateio_crawler import GateIoCrawler

options = webdriver.ChromeOptions()
# 팝업 차단을 활성화합니다.
options.add_argument('--disable-popup-blocking')
chrome_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
user_data_directory='/Users/kimminsu/Library/Application Support/Google/Chrome'
profile_directory='Profile 3'
options.add_argument(f"--user-data-dir={user_data_directory}")
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
options.add_argument(f"--profile-directory={profile_directory}")


# WebDriver 객체 생성
# driver = uc.Chrome( options = options,enable_cdp_events=True, version_main=120)
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver = webdriver.Chrome(options=options)


# selenium_stealth 설정
stealth(driver,
        vendor="Google Inc. ",
        platform="Win32",
        webgl_vendor="intel Inc. ",
        renderer= "Intel Iris OpenGL Engine",
        fix_hairline=True,
        headers=headers,
        )



# 웹사이트 방문
GateIoCrawler(driver).run()

# 대기 시간 설정 =&gt; 대기 시간을 설정하여, html이 렌더링 되는 시간을 벌어줍니다.
driver.implicitly_wait(2)

# 웹사이트에서 제목을 가져옵니다.
pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

input('Press any key to continue...')
driver.quit()


