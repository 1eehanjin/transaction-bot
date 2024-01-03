import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


with open('./secrets.json') as f:
            secret_data = json.load(f)
            metamask_password = secret_data["metamask_password"]
            user_data_dir = secret_data["user_data_dir"]


options = Options()


options.add_argument(f"user-data-dir={user_data_dir}")
options.add_argument("--profile-directory=profile 1")

options.add_experimental_option("detach", True)  # 화면이 꺼지지 않고 유지

options.add_argument("--start-maximized")  # 최대 크기로 시작

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)

driver.execute_script("window.open('about:blank', '_blank');")
time.sleep(3)

driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html")

time.sleep(3)
driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/form/div/div/input').send_keys(metamask_password)
driver.find_element("xpath", '//*[@id="app-content"]/div/div[2]/div/div/button').click()

# 탭 목록 가져오기
all_tabs = driver.window_handles

# 두 번째 탭으로 전환
driver.switch_to.window(all_tabs[1])

# 두 번째 탭에서 작업 수행
driver.get("https://qna3.ai/?code=kpKpcujE")
