import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

START_ACCOUNT_NUM = 12
END_ACCOUNT_NUM = 200

QUESTIONS = [
    "1. How can I access public data related to cryptocurrencies?",
    "2. What are the most popular cryptocurrencies in terms of market capitalization?",
    "3. Where can I find historical price data for Bitcoin?",
    "4. What is the current price of Ethereum?",
    "5. How does blockchain technology impact public data transparency?",
    "6. Can I use public data to predict cryptocurrency market trends?",
    "7. What are some government regulations affecting cryptocurrencies?",
    "8. How often is cryptocurrency market data updated?",
    "9. What is the role of public data in decentralized finance (DeFi) projects?",
    "10. How can I analyze the correlation between public data and cryptocurrency prices?",
    "11. Where can I find real-time cryptocurrency market data APIs?",
    "12. What are the key metrics to consider when evaluating a cryptocurrency's performance?",
    "13. How does public data contribute to cryptocurrency trading strategies?",
    "14. Are there any open datasets available for cryptocurrency research?",
    "15. What are the privacy implications of using public data in cryptocurrency analysis?",
    "16. How does government data affect the adoption of cryptocurrencies?",
    "17. What is the role of public data in initial coin offerings (ICOs)?",
    "18. What is the relationship between public data and crypto mining?",
    "19. How can I access public data on cryptocurrency wallets?",
    "20. What are the risks associated with using public data for cryptocurrency investments?",
    "21. How does sentiment analysis impact cryptocurrency trading based on public data?",
    "22. Are there any public data sources for tracking cryptocurrency transactions?",
    "23. What are the challenges of integrating public data into blockchain projects?",
    "24. How can I use public data to assess the security of a cryptocurrency exchange?",
    "25. How do cryptocurrency regulations vary from country to country?",
    "26. Can public data be used to detect cryptocurrency fraud?",
    "27. What is the impact of public data on cryptocurrency market volatility?",
    "28. How do cryptocurrency market trends influence public data sources?",
    "29. What are the advantages of using public data in cryptocurrency analytics?",
    "30. How can I build a cryptocurrency portfolio using public data?",
    "31. How does social media sentiment affect cryptocurrency prices?",
    "32. What role does public data play in the development of non-fungible tokens (NFTs)?",
    "33. How can I monitor cryptocurrency news using public data sources?",
    "34. What is the relationship between public data and decentralized exchanges (DEXs)?",
    "35. How does public data contribute to cryptocurrency research papers?",
    "36. What are the challenges of maintaining data accuracy in cryptocurrency analytics?",
    "37. How do public data breaches impact cryptocurrency security?",
    "38. How can I use public data to track the performance of a specific cryptocurrency project?",
    "39. What is the role of government agencies in regulating cryptocurrency markets?",
    "40. How do public data platforms impact the transparency of ICOs?",
    "41. Can public data be used for cryptocurrency arbitrage trading?",
    "42. How can I access public data on tokenomics and supply of cryptocurrencies?",
    "43. What are the ethical considerations when using public data for cryptocurrency analysis?",
    "44. How do cryptocurrency market cycles affect public data trends?",
    "45. How can I use public data to identify potential cryptocurrency investment opportunities?",
    "46. What are the implications of public data on cryptocurrency taxation?",
    "47. How does public data affect the evaluation of cryptocurrency projects for investment?",
    "48. What role does public data play in the governance of blockchain networks?",
    "49. How can I assess the liquidity of a cryptocurrency using public data?",
    "50. What are the emerging trends in the intersection of public data and cryptocurrencies?"
]


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
    def __init__(self):
        with open('./secrets.json') as f:
            secret_data = json.load(f)
            self.metamask_password = secret_data["metamask_password"]
            self.user_data_dir = secret_data["user_data_dir"]

    def open_browser(self):
        options = Options()
        options.add_argument(f"user-data-dir={self.user_data_dir}")
        options.add_argument(f"--profile-directory=profile 1")
        options.add_experimental_option("detach", True)
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.execute_script("window.open('about:blank', '_blank');")
        self.all_tabs = self.driver.window_handles
        self.wait = WebDriverWait(self.driver, LONG_WAIT_TIME)
        self.driver.implicitly_wait(LONG_WAIT_TIME)
        self.metamask_controller = MetamaskController(driver=self.driver, all_tabs=self.all_tabs, wait= self.wait)
        time.sleep(SHORT_WAIT_TIME)

    def work(self):
        self.metamask_controller.login(self.metamask_password)
        for i in range(START_ACCOUNT_NUM, END_ACCOUNT_NUM):
            self.perform_task(i)
        print(f"{START_ACCOUNT_NUM} ~ {END_ACCOUNT_NUM-1} 진행 완료되었습니다")

    def perform_task(self, account_number):
        while True:
            try:
                self.perform_normal_task(account_number=account_number)
                break
            except Exception as e:
                print(e)
                self.perform_error_task(account_number=account_number)

    def perform_normal_task(self, account_number):
        self.metamask_controller.remove_actions()
        self.metamask_controller.switch_account(account_number)
        self.referral_link = REFERRAL_LINKS[account_number//20]
        self.driver.get(self.referral_link)
        self.logout()
        self.login()
        time.sleep(SHORT_WAIT_TIME)
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
        self.metamask_controller.login(self.metamask_password)

    def logout(self):
        try:
            self.driver.find_element("class name", 'hidden.overflow-hidden.text-ellipsis.font-medium.text-white.md\\:block').click()
            self.driver.find_element(By.XPATH, "//*[contains(text(),'Sign Out')]").click()
        except:
            print("이미 로그아웃 되어있습니다.")    

    def login(self):
        connect_wallet_buttons = self.driver.find_elements("xpath",  "//*[contains(text(),'Connect Wallet')]")
        connect_wallet_buttons[-1].click()
        try:
            time.sleep(SHORT_WAIT_TIME)
            wallet_select_button = self.driver.find_element(By.XPATH, '/html/body/div[16]/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/button/div/div')
            self.wait.until(
                EC.element_to_be_clickable(wallet_select_button)
            )
            wallet_select_button.click()
        except:
            print("지갑선택창 스킵됨")
        self.metamask_controller.remove_actions()
        print("로그인 완료")

    def check_in(self):
        try:
            check_in_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Click To Check-in')]")
        except:
            print("이미 출석되어있습니다")
            return
        check_in_button.click()
        while not self.metamask_controller.confirm_transaction() and check_in_button.is_enabled:
            check_in_button.click()
        for i in range(10):
            try:
                self.driver.find_element(By.XPATH, "//button[contains(text(),'Claim Credits')]")
                print("출석 완료")
                return
            except:
                pass
        raise RuntimeError("출석이 완료되지 않습니다..")
        

    def switch_to_opbnb(self):
        chain_button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[2]")
        if not chain_button.text.find("opBNB"):
                print("이미 opBNB체인입니다")
                return
        chain_button.click()
        self.metamask_controller.remove_actions()
        print("출석체크 위해 opBNB 네트워크로 전환 완료")

    def send_qna(self):
        question = random.choice(QUESTIONS)
        textarea= self.driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/div[2]/div/div[1]/div[1]/div/div[1]/textarea')
        textarea.send_keys(question)
        textarea.send_keys(Keys.ENTER)
        answered  = False
        for i in range(5):
            try:
                good_button_container = self.driver.find_element("class name", 'flex.justify-end.gap-4')
                answered = True
                break
            except:
                pass
        if answered:
            good_button = good_button_container.find_element(By.XPATH, "./button")
            good_button.click()
            print("qna 및 따봉 완료")
            self.driver.get(self.referral_link)
            return True
        else:
            self.driver.delete_all_cookies()
            self.driver.get(self.referral_link)
            return False

    def vote(self, number):
        external_wallet_credits = self.driver.find_elements(By.CLASS_NAME, "text-lg")[-1].text
        external_wallet_credits = int(external_wallet_credits)
        if external_wallet_credits >= 5:
            vote_buttons = self.driver.find_elements(By.XPATH, "//*[text()='Vote']")
            vote_buttons[number].click()
            if self.metamask_controller.confirm_transaction():
                print(f"{number}번 보팅 완료") 
            else:
                raise RuntimeError("보팅 트랜잭션 승인 실패")
        else:
            print("크레딧 부족으로 보팅 스킵...")
        
     

class MetamaskController:
    def __init__(self, driver, all_tabs, wait):
        self.driver = driver
        self.all_tabs = all_tabs
        self.wait = wait
        
        
    def login(self, password):
        self.driver.switch_to.window(self.all_tabs[0])
        self.driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html")
        try:
            password_input = self.driver.find_element(
                By.XPATH, '//*[@id="password"]'
            )
        except Exception as e:
            print(e)
            raise RuntimeError("메타마스크 로그인 인풋이 로드되지 않습니다.")
        password_input.send_keys(password)
        self.driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/button').click()
        time.sleep(SHORT_WAIT_TIME)

    def switch_account(self, account_number):
        self.driver.switch_to.window(self.all_tabs[0])
        account_change_button = self.driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/button')
        if account_change_button.text == f'계정 {account_number}':
            print(f"** 이미 메타마스크 계정 {account_number}입니다.")
        else:
            account_change_button.click()
            time.sleep(SHORT_WAIT_TIME)
            self.driver.find_element(By.XPATH, f"//*[text()='계정 {account_number}']").click()
            time.sleep(SHORT_WAIT_TIME)
            print(f"** 메타마스크 계정 {account_number}으로 전환되었습니다.")
        self.driver.switch_to.window(self.all_tabs[1])
    
    def remove_actions(self):
        self.driver.switch_to.window(self.all_tabs[0])
        while True:
            time.sleep(SHORT_WAIT_TIME)
            self.driver.refresh()
            try:
                button = self.driver.find_element(By.XPATH, "//button[contains(text(), '네트워크 전환') or contains(text(), '서명') or contains(text(), '컨펌') or contains(text(), '활동') ]")
                if button.text == '컨펌':
                    self.driver.find_element(By.XPATH, "//button[contains(text(), '거부')]").click()
                elif button.text == '네트워크 전환' or button.text == '서명':
                    button.click()    
                else: 
                    break
            except Exception as e:
                print(e)
                raise RuntimeError("메마 액션지우기중 에러 발생")
        self.driver.switch_to.window(self.all_tabs[1])

    def confirm_transaction(self):
        self.driver.switch_to.window(self.all_tabs[0])
        time.sleep(SHORT_WAIT_TIME)
        self.driver.refresh()
        try:
            confirm_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '컨펌')]")
            self.wait.until(
                EC.element_to_be_clickable(confirm_button)
            )
            confirm_button.click()
            time.sleep(SHORT_WAIT_TIME)
            print("트랜잭션 버튼 클릭")
            result =  True
        except:
            print("트랜잭션 버튼 클릭 실패")
            self.remove_actions()
            result = False
        finally:
            self.driver.switch_to.window(self.all_tabs[1])
            return result
    

if __name__ == "__main__":
    try:
        chrome_controller = ChromeController()
        chrome_controller.open_browser()
        if IS_SETTING_MODE:
            print("설정을 위해 봇을 실행하지 않습니다.")
        else:
            chrome_controller.work()
    except Exception as e:
        print(e)
        message_sender.send_telegram_message("qna봇 재실행 필요한 오류 발생")

