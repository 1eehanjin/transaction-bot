import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

SHORT_WAIT_TIME = 2
LONG_WAIT_TIME =10

def print_page_html():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.text)

def log_in():
    try:
        login_button = driver.find_element("xpath", "//*[contains(text(),'Sign In')]")
    except:
         print("이미 로그인 되어있습니다")
         return
    login_button.click()
    time.sleep(SHORT_WAIT_TIME)
    driver.find_element("xpath", '/html/body/div[5]/div/div/div/div/div[2]/div/button').click()
    time.sleep(SHORT_WAIT_TIME)
    try:
        driver.find_element("xpath", '/html/body/div[18]/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/button').click()
    except:
         print("지갑선택창 스킵됨")

def confirm_network_and_sign():
    driver.switch_to.window(all_tabs[0])
    time.sleep(SHORT_WAIT_TIME)
    while True:
        driver.refresh()
        time.sleep(SHORT_WAIT_TIME)
        if not confirm_network() and not confirm_sign():
             break
    driver.switch_to.window(all_tabs[1])
    print("메타마스크 네트워크 전환, 사인창 확인 완료")
    time.sleep(SHORT_WAIT_TIME)
    

def confirm_network():
    try:
        driver.find_element("xpath", "//button[contains(text(),'네트워크 전환')]").click()
        time.sleep(SHORT_WAIT_TIME)
        return True
    except:
        return False

def confirm_sign():
    try:
        driver.find_element("xpath", "//button[contains(text(),'서명')]").click()
        time.sleep(SHORT_WAIT_TIME)
        return True
    except:
        return False


def confirm_transaction():
    driver.switch_to.window(all_tabs[0])
    time.sleep(SHORT_WAIT_TIME)
    driver.refresh()
    time.sleep(SHORT_WAIT_TIME)
    try:
        driver.find_element("xpath", "//button[contains(text(),'컨펌')]").click()
        time.sleep(SHORT_WAIT_TIME)
    except:
         print("전송할 트랜잭션이 없습니다.")  
    driver.switch_to.window(all_tabs[1])
    time.sleep(SHORT_WAIT_TIME)
    print("트랜잭션 전송 완료")
    

def check_in():
    try:
        check_in_button = driver.find_element("xpath", "//button[contains(text(),'Click To Check-in')]")
    except:
         print("이미 출석되어있습니다")
         return
    check_in_button.click()
    time.sleep(SHORT_WAIT_TIME)
    confirm_network_and_sign()
    confirm_transaction()
    time.sleep(SHORT_WAIT_TIME)
    print("출석 완료")

def switch_to_opbnb():
    chain_button = driver.find_element("xpath", "/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[2]")
    if not chain_button.text.find("opBNB"):
            print("이미 opBNB체인입니다")
            return
    chain_button.click()
    time.sleep(SHORT_WAIT_TIME)
    confirm_network_and_sign()
    driver.switch_to.window(all_tabs[1])
    time.sleep(SHORT_WAIT_TIME)
    print("출석체크 위해 opBNB 네트워크로 전환 완료")

def qna(question):
     textarea= driver.find_element("xpath", '//*[@id="root"]/div[1]/div/div[2]/div/div[1]/div[1]/div/div[1]/textarea')
     textarea.send_keys(question)
     textarea.send_keys(Keys.ENTER)
     time.sleep(LONG_WAIT_TIME)
     good_button_container = driver.find_element("class name", 'flex.justify-end.gap-4')
     good_button = good_button_container.find_element("xpath", "./button")
     good_button.click()
     time.sleep(SHORT_WAIT_TIME)
     print("qna 및 따봉 완료")
     driver.get("https://qna3.ai/")
     time.sleep(LONG_WAIT_TIME)

def vote(number):
    vote_buttons = driver.find_elements("xpath", "//*[text()='Vote']")
    vote_buttons[number].click()
    time.sleep(SHORT_WAIT_TIME)
    confirm_network_and_sign()
    confirm_transaction()
    print("보팅 완료") 
    driver.get("https://qna3.ai")
    time.sleep(LONG_WAIT_TIME)
     

with open('./secrets.json') as f:
            secret_data = json.load(f)
            metamask_password = secret_data["metamask_password"]
            user_data_dir = secret_data["user_data_dir"]


options = Options()
options.add_argument(f"user-data-dir={user_data_dir}")
options.add_argument("--profile-directory=profile 4")
options.add_experimental_option("detach", True)  # 화면이 꺼지지 않고 유지
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.execute_script("window.open('about:blank', '_blank');")
all_tabs = driver.window_handles
time.sleep(SHORT_WAIT_TIME)

driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html")
time.sleep(SHORT_WAIT_TIME)
driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/form/div/div/input').send_keys(metamask_password)
driver.find_element("xpath", '//*[@id="app-content"]/div/div[2]/div/div/button').click()

driver.switch_to.window(all_tabs[1])
driver.get("https://qna3.ai/?code=kpKpcujE")
time.sleep(LONG_WAIT_TIME)


try:
    log_in()
    confirm_network_and_sign()
    qna("What is Sleepless AI and why is it so popular?")
    vote(0)
    switch_to_opbnb()
    check_in()
except Exception as e:
    print(f"오류가 발생했습니다: {e}")
    print_page_html()
finally:
    driver.switch_to.window(all_tabs[1])



