import pickle
import undetected_chromedriver as uc
from selenium_stealth import stealth

from v2.modules.gateio_crawler import GateIoCrawler

options = uc.ChromeOptions()
# 팝업 차단을 활성화합니다.
options.add_argument('--disable-popup-blocking')
chrome_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
user_data_directory='/Users/kimminsu/Library/Application Support/Google/Chrome'
profile_directory='Profile 3'
options.add_argument(f"--user-data-dir={user_data_directory}")
options.add_argument(f"--profile-directory={profile_directory}")

# WebDriver 객체 생성
driver = uc.Chrome( options = options,enable_cdp_events=True,incognito=True)

# selenium_stealth 설정
stealth(driver,
        vendor="Google Inc. ",
        platform="Win32",
        webgl_vendor="intel Inc. ",
        renderer= "Intel Iris OpenGL Engine",
        fix_hairline=True,
        )



# 웹사이트 방문
GateIoCrawler(driver).run()

# 대기 시간 설정 =&gt; 대기 시간을 설정하여, html이 렌더링 되는 시간을 벌어줍니다.
driver.implicitly_wait(2)

# 웹사이트에서 제목을 가져옵니다.
pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

input('Press any key to continue...')
driver.quit()


