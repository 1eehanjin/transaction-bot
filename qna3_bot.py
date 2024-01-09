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

QUESTIONS = ['What is the connection between cryptocurrency and the city of Chungju?',
 'Are there any cryptocurrency businesses or exchanges operating in Chungju?',
 'How does Chungju City view the adoption of cryptocurrencies?',
 "Can you explain the impact of cryptocurrency on Chungju's economy?",
 'Are there any cryptocurrency-related events or conferences held in Chungju?',
 'What cryptocurrency regulations are in place in Chungju?',
 'Are there any blockchain startups based in Chungju?',
 'How are cryptocurrency transactions taxed in Chungju?',
 'Does Chungju City promote blockchain technology development?',
 'Are there any cryptocurrency mining activities in Chungju?',
 'Have there been any cryptocurrency-related scams reported in Chungju?',
 'How does the local government of Chungju support blockchain innovation?',
 'Are there any cryptocurrency ATMs in Chungju?',
 'What is the level of cryptocurrency adoption among Chungju residents?',
 'Are there any educational programs on cryptocurrency and blockchain in '
 'Chungju?',
 'How does Chungju City regulate Initial Coin Offerings (ICOs)?',
 'Are there any cryptocurrency meetups or communities in Chungju?',
 'Does Chungju have any plans to issue its own cryptocurrency?',
 'How does Chungju City ensure the security of cryptocurrency users?',
 'What is the stance of Chungju City on decentralized finance (DeFi)?',
 'Are there any notable cryptocurrency investors or companies headquartered in '
 'Chungju?',
 'How does Chungju City address the environmental concerns of cryptocurrency '
 'mining?',
 'What are the potential benefits of cryptocurrency for businesses in Chungju?',
 'Are there any cryptocurrency-related research institutions in Chungju?',
 'How does Chungju City promote blockchain-based solutions for public '
 'services?',
 'What are the challenges faced by cryptocurrency businesses in Chungju?',
 'Does Chungju City collaborate with blockchain projects for urban '
 'development?',
 'How does Chungju City ensure the legality of cryptocurrency transactions?',
 'Are there any cryptocurrency trading restrictions for residents of Chungju?',
 'Does Chungju City plan to integrate blockchain technology into its '
 'administrative processes?',
 'Are there any regulations on cryptocurrency advertising in Chungju?',
 'How does Chungju City protect consumers from cryptocurrency fraud?',
 'Are there any partnerships between Chungju City and blockchain companies?',
 'Does Chungju have a strategy for attracting cryptocurrency investment?',
 "What is the role of blockchain in Chungju's smart city initiatives?",
 'How does Chungju City address the energy consumption concerns of '
 'cryptocurrency mining?',
 'Are there any cryptocurrency-related job opportunities in Chungju?',
 'How does Chungju City educate its residents about cryptocurrency risks?',
 'Does Chungju City have a blockchain-based voting system?',
 'How does Chungju City handle cryptocurrency donations for charitable '
 'purposes?',
 'Are there any local businesses in Chungju that accept cryptocurrency '
 'payments?',
 'How does Chungju City balance the innovation potential of cryptocurrency '
 'with regulatory concerns?',
 'Are there any government grants or incentives for cryptocurrency startups in '
 'Chungju?',
 'How does Chungju City collaborate with universities on blockchain research?',
 "What is the role of cryptocurrency in Chungju's tourism industry?",
 'Are there any cryptocurrency trading competitions or events in Chungju?',
 'How does Chungju City approach the issue of cryptocurrency price volatility?',
 'Are there any cryptocurrency-related art or cultural events in Chungju?',
 'What is the role of blockchain in land and property records in Chungju?',
 'How does Chungju City engage with the global cryptocurrency community?']

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

class ChromeController:

    def open_browser(self):
        options = Options()
        options.add_argument(f"user-data-dir={user_data_dir}")
        options.add_argument(f"--profile-directory=profile 1")
        options.add_experimental_option("detach", True)  # 화면이 꺼지지 않고 유지
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.execute_script("window.open('about:blank', '_blank');")
        self.all_tabs = self.driver.window_handles
        time.sleep(SHORT_WAIT_TIME)

    def work(self):
        self.metamask_login()
        for i in range(START_ACCOUNT_NUM, END_ACCOUNT_NUM):
            self.perform_task(i)
        print(f"{START_ACCOUNT_NUM} ~ {END_ACCOUNT_NUM-1} 진행 완료되었습니다")

    def metamask_login(self):
        self.driver.switch_to.window(self.all_tabs[0])
        self.driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html")
        time.sleep(SHORT_WAIT_TIME)
        self.driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/form/div/div/input').send_keys(metamask_password)
        self.driver.find_element("xpath", '//*[@id="app-content"]/div/div[2]/div/div/button').click()
        time.sleep(SHORT_WAIT_TIME)

    def perform_task(self, account_number):
        while True:
            try:
                self.perform_normal_task(account_number=account_number)
                break
            except Exception as e:
                print(1)
                self.perform_error_task(account_number=account_number)

    def perform_normal_task(self, account_number):
        self.switch_metamask_account(account_number)
        self.referral_link = REFERRAL_LINKS[account_number//20]
        self.driver.get(self.referral_link)
        time.sleep(LONG_WAIT_TIME)
        self.log_out()
        self.log_in()
        while self.send_qna() != True:
            print("답변을 생성하지 못해 재질문합니다 ... ")
        self.vote(0)
        #self.vote(1)
        #self.vote(2)
        self.switch_to_opbnb()
        self.check_in()
        print(f">>{account_number}번 완료")

    def perform_error_task(self, account_number):
        print(f"!!{account_number}번 진행중 오류가 발생했습니다\n")
        message_sender.send_telegram_message(f"!!qna3 {account_number}번계정 진행중 오류가 발생했습니다")
        self.driver.delete_all_cookies()
        self.driver.quit()
        self.open_browser()
        self.metamask_login()

    def switch_metamask_account(self, account_number):
        self.driver.switch_to.window(self.all_tabs[0])
        self.driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html")
        time.sleep(SHORT_WAIT_TIME)
        self.confirm_network_and_sign_and_transaction()
        self.driver.switch_to.window(self.all_tabs[0])
        account_change_button = self.driver.find_element("xpath", '//*[@id="app-content"]/div/div[2]/div/button111')
        if account_change_button.text == f'계정 {account_number}':
            print(f"** 이미 메타마스크 계정 {account_number}입니다.")
        else:
            account_change_button.click()
            time.sleep(SHORT_WAIT_TIME)
            self.driver.find_element("xpath", f"//*[text()='계정 {account_number}']").click()
            time.sleep(SHORT_WAIT_TIME)
            print(f"** 메타마스크 계정 {account_number}으로 전환되었습니다.")
        self.driver.switch_to.window(self.all_tabs[1])

    def log_out(self):
        try:
            self.driver.find_element("class name", 'hidden.overflow-hidden.text-ellipsis.font-medium.text-white.md\\:block').click()
            time.sleep(SHORT_WAIT_TIME)
            self.driver.find_element("xpath", "//*[contains(text(),'Sign Out')]").click()
            time.sleep(SHORT_WAIT_TIME)
        except:
            print("이미 로그아웃 되어있습니다.")    

    def log_in(self):
        self.driver.find_element("xpath",  '//*[@id="root"]/div[1]/div/div[2]/div/div[2]/div/div[1]/div[3]/div/div/div[3]/div/div[1]/div/button').click()
        time.sleep(SHORT_WAIT_TIME)
        try:
            self.driver.find_element("xpath", '/html/body/div[16]/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/button/div/div').click()
        except:
            print("지갑선택창 스킵됨")
        self.confirm_network_and_sign_and_transaction()
        print("로그인 완료")

    def confirm_network_and_sign_and_transaction(self):
        self.driver.switch_to.window(self.all_tabs[0])
        time.sleep(SHORT_WAIT_TIME)
        while True:
            self.driver.refresh()
            time.sleep(SHORT_WAIT_TIME)
            if not self.confirm_network() and not self.confirm_sign() and not self.confirm_transaction():
                break            
        self.driver.switch_to.window(self.all_tabs[1])
        print("메타마스크 네트워크 전환, 서명 요청, 트랜잭션 요청 제거 완료")
        time.sleep(SHORT_WAIT_TIME)
        
    def confirm_network(self):
        try:
            self.driver.find_element("xpath", "//button[contains(text(),'네트워크 전환')]").click()
            time.sleep(SHORT_WAIT_TIME)
            return True
        except:
            return False

    def confirm_sign(self):
        try:
            self.driver.find_element("xpath", "//button[contains(text(),'서명')]").click()
            time.sleep(SHORT_WAIT_TIME)
            return True
        except:
            return False


    def confirm_transaction(self):
        try:
            confirm_button = self.driver.find_element("xpath", "//button[contains(text(),'컨펌')]")
            time.sleep(SHORT_WAIT_TIME)
            print("트랜잭션 버튼 발견")
        except:
            return False
        for i in range(10):
            try:
                confirm_button.click()
                break
            except:
                print("트랜잭션 버튼 활성화 대기중...")  
                time.sleep(SHORT_WAIT_TIME)
        self.driver.switch_to.window(self.all_tabs[1])
        return True

    def check_in(self):
        try:
            check_in_button = self.driver.find_element("xpath", "//button[contains(text(),'Click To Check-in')]")
        except:
            print("이미 출석되어있습니다")
            return
        check_in_button.click()
        time.sleep(SHORT_WAIT_TIME)
        self.confirm_network_and_sign_and_transaction()
        time.sleep(SHORT_WAIT_TIME)
        print("출석 완료")

    def switch_to_opbnb(self):
        chain_button = self.driver.find_element("xpath", "/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[2]")
        if not chain_button.text.find("opBNB"):
                print("이미 opBNB체인입니다")
                return
        chain_button.click()
        time.sleep(SHORT_WAIT_TIME)
        self.confirm_network_and_sign_and_transaction()
        time.sleep(SHORT_WAIT_TIME)
        print("출석체크 위해 opBNB 네트워크로 전환 완료")

    def send_qna(self):
        question = random.choice(QUESTIONS)
        textarea= self.driver.find_element("xpath", '//*[@id="root"]/div[1]/div/div[2]/div/div[1]/div[1]/div/div[1]/textarea')
        textarea.send_keys(question)
        textarea.send_keys(Keys.ENTER)
        time.sleep(LONG_WAIT_TIME)
        count = 0
        while True:
            if count == 2:
                self.driver.refresh()
                time.sleep(LONG_WAIT_TIME)
            if count == 4:
                self.driver.delete_all_cookies()
                time.sleep(LONG_WAIT_TIME)
                self.driver.get(self.referral_link)
                time.sleep(LONG_WAIT_TIME)
                return False
            try:
                good_button_container = self.driver.find_element("class name", 'flex.justify-end.gap-4')
                break
            except:
                print("아직 질문에 대한 답변이 생성되지 않았습니다..")
                count +=1
                time.sleep(LONG_WAIT_TIME)
        good_button = good_button_container.find_element("xpath", "./button")
        good_button.click()
        time.sleep(SHORT_WAIT_TIME)
        print("qna 및 따봉 완료")
        self.driver.get(self.referral_link)
        time.sleep(LONG_WAIT_TIME)
        return True

    def vote(self, number):
        vote_buttons = self.driver.find_elements("xpath", "//*[text()='Vote']")
        vote_buttons[number].click()
        time.sleep(SHORT_WAIT_TIME)
        self.confirm_network_and_sign_and_transaction()
        print(f"{number}번 보팅 완료") 
        time.sleep(LONG_WAIT_TIME)
     

try:
    with open('./secrets.json') as f:
                secret_data = json.load(f)
                metamask_password = secret_data["metamask_password"]
                user_data_dir = secret_data["user_data_dir"]
    chrome_controller = ChromeController()
    chrome_controller.open_browser()
    if IS_SETTING_MODE:
        print("설정을 위해 봇을 실행하지 않습니다.")
    else:
        chrome_controller.work()
except Exception as e:
    print(e)
    message_sender.send_telegram_message("qna봇 재실행 필요한 오류 발생")

