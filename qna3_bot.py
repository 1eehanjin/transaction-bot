import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import random
import message_sender

"""
1. secrets.json 파일 만들어서
    {
        "user_data_dir": "구글 데이터 저장할 새로운 폴더 경로", 
        "metamask_password": "메타마스크 로그인 비밀번호(버너지갑)"
    }
    적고 저장
    * user_data_dir는 기존 구글 데이터가 있는 폴더가 아니라 아예 새로운 구글 데이터를 저장할 임의의 새폴더를 만들고 적어놓기
2. 크롬드라이버 버전맞춰 다운로드, 파이썬 패키지 다운로드(pip install ~) *인터넷 '파이썬 selenium 사용법' 참고
3. IS_SETTING_MODE = True로 하여 크롬 열고  메타마스크 계정 설정
    - 아예 새로운 프로필로 크롬 잘 열리는지 확인하고(프로필이 하나만 있어야 함)
    - 메타마스크 다운로드, 지갑 새로 만들고, 계정 하나 추가해보기
    - 돌릴 계정의 이름이 "계정 2" < 양식인지 확인한다. 
        - 아마 첫번째 계정은 'Account 1'로 되어있을 텐데 이거때문에 START_ACCOUNT_NUM 2로 돌려야할 듯. (계정 1로 수정 안된다)
        - 메타마스크 언어도 한글로 설정해놔야 한다.
    - 메타마스크 계정 왕창 추가
    - 각 계정별 BNB, opBNB 극소량(최소출금 0.009) 보내놓기 (하나라도 빼먹으면 중간에 오류 발생)
    - qna3.ai 처음 접속하고
        - Sign in 누르고 'Metamask로 사이트 연결' 모든 계정 체크해서 연결해놓기. (서명하고 다르다)
            * 모든 계정이 사이트에 연결이 되지 않은 상태에서 연결을 시도할 시 일괄 체크할 수 있는 창이 나오고, 하나라도 연결된 계정이 있으면 하나씩만 연결이 가능한데,
            * 일괄 연결을 위해서 메타마스크에서 '...' -> '연결된 사이트' -> qna3 '연결 해제'-> '모든 계정 연결 해제' 뒤 연결하면 일괄 연결이 가능하다.
        - BNB, opBNB 추가(qna홈페이지에서 전환 한 번씩)
        - 메타마스크 새로고침해서 처음 뜨는 '새로운 소식' 팝업도 한번 닫아주고 돌려야한다.
4. 바로 밑의 상수 변경
    - 중간중간 기다리는 시간
    - 시작 계정 번호, 끝나는 계정 번호( 내 마지막 계정 번호 +1 )
    - 질문 목록
    - 레퍼럴 링크 목록
        * 본인 레퍼럴 링크로 꼭 변경 . 돌릴 계정 수 / 20 개는 넣어놔야 한다.
5. IS_SETTING_MODE = False로 바꾸고 실행 
6. 실행하자마자 오류나면 크롬 이 프로필 창 실행되고있나 체크 !
7. vote 수정하려면 299번 ~ 301번 줄에서 vote(0) vote(1) vote(2) 부분 지우거나 숫자 바꾸면 된다(숫자는 n번째 Vote 버튼 클릭 의미)
8. 실행 전 꼭 저장하고 시작
"""
IS_SETTING_MODE = False

SHORT_WAIT_TIME = 2
LONG_WAIT_TIME = 10

START_ACCOUNT_NUM = 2
END_ACCOUNT_NUM = 200

QUESTIONS = ["How did South Korea's victory at the 2023 League of Legends World "
 'Championship impact the cryptocurrency market?',
 "Did South Korea's victory in the League of Legends World Championship lead "
 'to increased interest in cryptocurrencies?',
 'What were the trends in cryptocurrency investments in South Korea following '
 'the 2023 League of Legends World Championship win?',
 'Did the influx of funds into the South Korean cryptocurrency market show any '
 'specific patterns after the victory in the 2023 League of Legends World '
 'Championship?',
 'Are there any similarities between the cryptocurrency industry and the world '
 'of esports in South Korea?',
 "Did South Korea's success in the 2023 League of Legends World Championship "
 'influence the adoption of blockchain technology?',
 'How did South Korean investors react to the victory in terms of '
 'cryptocurrency trading?',
 'Were there any notable cryptocurrency projects or initiatives launched in '
 'South Korea after the 2023 League of Legends World Championship win?',
 'Did the victory in the esports industry affect the perception of '
 'cryptocurrencies in South Korea?',
 'Were there any crypto-related sponsorship deals or partnerships related to '
 'the 2023 League of Legends World Championship?',
 'How did South Korean esports organizations leverage cryptocurrencies and '
 'blockchain technology?',
 'Did the winning esports team or players receive cryptocurrency rewards or '
 'endorsements?',
 'Were there any specific cryptocurrencies or tokens associated with the 2023 '
 'League of Legends World Championship in South Korea?',
 'Did the event lead to discussions about creating a dedicated esports '
 'cryptocurrency or token?',
 'How did South Korean regulators react to the intersection of esports and '
 'cryptocurrencies after the championship win?',
 "Did South Korea's esports industry explore blockchain-based voting or "
 'governance systems?',
 'Were there any esports-related NFT (Non-Fungible Token) projects in South '
 'Korea following the championship?',
 'Did the victory lead to increased blockchain gaming development in South '
 'Korea?',
 'Were there any changes in cryptocurrency exchange regulations in South Korea '
 'post-2023 League of Legends World Championship?',
 'Did the event affect the adoption of decentralized finance (DeFi) in South '
 'Korea?',
 'Were there any esports-themed cryptocurrency events or conferences in South '
 'Korea?',
 'Did the victory result in a surge in trading volumes for esports-related '
 'tokens in South Korea?',
 'How did the South Korean government respond to the potential synergies '
 'between esports and cryptocurrency?',
 'Were there any partnerships between esports teams and cryptocurrency '
 'projects in South Korea?',
 'Did the victory lead to an increase in cryptocurrency education and '
 'awareness campaigns in South Korea?',
 "How did South Korea's victory influence the sentiment of South Korean "
 'cryptocurrency enthusiasts?',
 'Were there any blockchain-based solutions introduced for esports tournament '
 'management in South Korea?',
 'Did the event trigger discussions about tokenizing esports assets in South '
 'Korea?',
 'How did the South Korean esports community react to the integration of '
 'cryptocurrencies?',
 'Were there any initiatives to reward esports fans with cryptocurrencies in '
 'South Korea?',
 'How did esports players and teams manage their earnings from cryptocurrency '
 'sponsorships?',
 'Were there any cryptocurrency endorsements or collaborations involving South '
 'Korean esports players?',
 'Did South Korean universities offer blockchain and cryptocurrency-related '
 'courses following the championship?',
 'How did South Korean esports organizations leverage blockchain for fan '
 'engagement?',
 'Were there any esports-related blockchain games or platforms introduced in '
 'South Korea?',
 'How did South Korean cryptocurrency exchanges promote esports-related '
 'tokens?',
 "Were there any NFT collectibles associated with South Korea's victory at the "
 '2023 League of Legends World Championship?',
 'Did the event lead to an increase in blockchain-based ticketing solutions '
 'for esports events in South Korea?',
 'How did South Korean esports teams use blockchain technology for talent '
 'scouting and management?',
 'Were there any esports-specific cryptocurrency wallets or payment solutions '
 'introduced in South Korea?',
 'How did the victory impact the overall esports and blockchain ecosystem in '
 'South Korea?',
 'Were there any cryptocurrency-focused hackathons or innovation competitions '
 'related to esports in South Korea?',
 'How did the event affect the tokenization of esports content in South Korea?',
 'Were there any blockchain-based platforms for esports betting introduced in '
 'South Korea?',
 'How did South Korean esports players and teams handle cryptocurrency '
 'taxation issues?']

REFERRAL_LINKS = [
    "https://qna3.ai/?code=kpKpcujE", #0~19번
    "https://qna3.ai/?code=H58QpM6s", #20~39번 계정2
    "https://qna3.ai/?code=PKTexRsB", #40~59번 계정3
    "https://qna3.ai/?code=JuAfuffW",
    "https://qna3.ai/?code=MWfhWuPc",
    "https://qna3.ai/?code=bwPDrEp3",
    "https://qna3.ai/?code=g9XR4UEW",
    "https://qna3.ai/?code=VNDR6rJH",
    "https://qna3.ai/?code=z97hpb36",
    "https://qna3.ai/?code=3a5wgqZc"
]

def metamask_login():
    driver.switch_to.window(all_tabs[0])
    driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html")
    time.sleep(SHORT_WAIT_TIME)
    driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/form/div/div/input').send_keys(metamask_password)
    driver.find_element("xpath", '//*[@id="app-content"]/div/div[2]/div/div/button').click()
    time.sleep(SHORT_WAIT_TIME)

def switch_metamask_account(account_number):
    #계정 전환
    driver.switch_to.window(all_tabs[0])
    driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html")
    time.sleep(SHORT_WAIT_TIME)
    account_change_button = driver.find_element("xpath", '//*[@id="app-content"]/div/div[2]/div/button')
    if account_change_button.text == f'계정 {account_number}':
        print(f"** 이미 메타마스크 계정 {account_number}입니다.")
    else:
        account_change_button.click()
        time.sleep(SHORT_WAIT_TIME)
        driver.find_element("xpath", f"//*[text()='계정 {account_number}']").click()
        time.sleep(SHORT_WAIT_TIME)
        print(f"** 메타마스크 계정 {account_number}으로 전환되었습니다.")
    driver.switch_to.window(all_tabs[1])

def print_page_html():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.text)

def log_out():
    try:
        driver.find_element("class name", 'hidden.overflow-hidden.text-ellipsis.font-medium.text-white.md\\:block').click()
        time.sleep(SHORT_WAIT_TIME)
        driver.find_element("xpath", "//*[contains(text(),'Sign Out')]").click()
        time.sleep(SHORT_WAIT_TIME)
    except:
        print("이미 로그아웃 되어있습니다.")    

def log_in():
    driver.find_element("xpath",  '//*[@id="root"]/div[1]/div/div[2]/div/div[2]/div/div[1]/div[3]/div/div/div[3]/div/div[1]/div/button').click()
    time.sleep(SHORT_WAIT_TIME)
    try:
        driver.find_element("xpath", '/html/body/div[16]/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/button/div/div').click()
    except:
         print("지갑선택창 스킵됨")
    print("로그인 완료")

def confirm_network_and_sign():
    driver.switch_to.window(all_tabs[0])
    time.sleep(SHORT_WAIT_TIME)
    while True:
        driver.refresh()
        time.sleep(SHORT_WAIT_TIME)
        if not confirm_network() and not confirm_sign():
             break
    driver.switch_to.window(all_tabs[1])
    print("메타마스크 네트워크 전환, 서명 요청 제거 완료")
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
    for i in range(5):
        try:
            driver.find_element("xpath", "//button[contains(text(),'컨펌')]").click()
            break
        except:
            print("트랜잭션 버튼 활성화 대기중...")  
            time.sleep(SHORT_WAIT_TIME)
    if i == 4:
        print("트랜잭션 버튼을 찾지 못했습니다...원래 화면으로 되돌아갑니다.")
    else:
        print("트랜잭션 전송 성공")
    time.sleep(SHORT_WAIT_TIME)
    driver.switch_to.window(all_tabs[1])
    time.sleep(SHORT_WAIT_TIME)
    

def check_in():
    try:
        check_in_button = driver.find_element("xpath", "//button[contains(text(),'Click To Check-in')]")
    except:
         print("이미 출석되어있습니다")
         return
    check_in_button.click()
    time.sleep(SHORT_WAIT_TIME)
    #confirm_network_and_sign()
    confirm_transaction()
    time.sleep(LONG_WAIT_TIME)
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

def send_qna():
     question = random.choice(QUESTIONS)
     textarea= driver.find_element("xpath", '//*[@id="root"]/div[1]/div/div[2]/div/div[1]/div[1]/div/div[1]/textarea')
     textarea.send_keys(question)
     textarea.send_keys(Keys.ENTER)
     time.sleep(LONG_WAIT_TIME)
     count = 0
     while True:
        if count == 2:
            driver.refresh()
            time.sleep(LONG_WAIT_TIME)
        if count == 4:
            driver.delete_all_cookies()
            time.sleep(LONG_WAIT_TIME)
            driver.get(referral_link)
            time.sleep(LONG_WAIT_TIME)
            return False
        try:
            good_button_container = driver.find_element("class name", 'flex.justify-end.gap-4')
            break
        except:
            print("아직 질문에 대한 답변이 생성되지 않았습니다..")
            count +=1
            time.sleep(LONG_WAIT_TIME)
     good_button = good_button_container.find_element("xpath", "./button")
     good_button.click()
     time.sleep(SHORT_WAIT_TIME)
     print("qna 및 따봉 완료")
     driver.get(referral_link)
     time.sleep(LONG_WAIT_TIME)
     return True

def vote(number):
    vote_buttons = driver.find_elements("xpath", "//*[text()='Vote']")
    vote_buttons[number].click()
    time.sleep(SHORT_WAIT_TIME)
    confirm_transaction()
    print(f"{number}번 보팅 완료") 
    time.sleep(LONG_WAIT_TIME)
     


with open('./secrets.json') as f:
            secret_data = json.load(f)
            metamask_password = secret_data["metamask_password"]
            user_data_dir = secret_data["user_data_dir"]
options = Options()
options.add_argument(f"user-data-dir={user_data_dir}")
options.add_argument(f"--profile-directory=profile 1")
options.add_experimental_option("detach", True)  # 화면이 꺼지지 않고 유지
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.execute_script("window.open('about:blank', '_blank');")
all_tabs = driver.window_handles
time.sleep(SHORT_WAIT_TIME)

if IS_SETTING_MODE:
    print("설정을 위해 봇을 실행하지 않습니다.")
else:
    metamask_login()
    for i in range(START_ACCOUNT_NUM, END_ACCOUNT_NUM):
        try:
            confirm_network_and_sign()
            switch_metamask_account(i)
            confirm_network_and_sign()
            referral_link = REFERRAL_LINKS[i//20]
            driver.get(referral_link)
            time.sleep(LONG_WAIT_TIME)
            print(f"{i}번 레퍼럴링크:  {referral_link}")
            log_out()
            log_in()
            confirm_network_and_sign()
            while send_qna() != True:
                print("답변을 생성하지 못해 재질문합니다 ... ")
            #vote(0)
            #vote(1)
            #vote(2)
            switch_to_opbnb()
            check_in()
            print(f">>{i}번 완료")
        except Exception as e:
            print(f"!!{i}번 진행중 오류가 발생했습니다\n{e}")
            message_sender.send_telegram_message(f"!!qna3 {i}번계정 진행중 오류가 발생했습니다")
            driver.delete_all_cookies()
            confirm_network_and_sign()
            confirm_transaction()
            i = i - 1
            driver.quit()
            options = Options()
            options.add_argument(f"user-data-dir={user_data_dir}")
            options.add_argument(f"--profile-directory=profile 1")
            options.add_experimental_option("detach", True)  # 화면이 꺼지지 않고 유지
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            driver.execute_script("window.open('about:blank', '_blank');")
            all_tabs = driver.window_handles
            time.sleep(SHORT_WAIT_TIME)
            metamask_login()
        finally:
            driver.switch_to.window(all_tabs[1])
    print(f"{START_ACCOUNT_NUM} ~ {END_ACCOUNT_NUM-1} 진행 완료되었습니다")


