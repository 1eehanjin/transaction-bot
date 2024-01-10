import pprint
import time
from qna3_bot import ChromeController
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pyperclip

SHORT_WAIT_TIME = 2
MAX = 201
class MetamaskAccountGenerator(ChromeController):
    def append_account_address_list(self, account_number):
        try:
            self.metamask_controller.switch_account(account_number)
        except:
            self.generate_new_account()
            print(f"$$ 메타마스크 계정 {account_number} 생성했습니다.")
        finally:
            self.retrieve_account_address()

    def generate_new_account(self):
        # self.driver.switch_to.window(self.all_tabs[0])
        # account_change_button = self.driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/button')
        # account_change_button.click()
        self.driver.find_element(By.XPATH, "//*[text()='Add account or hardware wallet']").click()
        self.driver.find_element(By.XPATH, "//*[text()='Add a new account']").click()
        self.driver.find_element(By.XPATH, "//*[text()='생성']").click()
        self.driver.switch_to.window(self.all_tabs[1])

    def retrieve_account_address(self):
        self.driver.switch_to.window(self.all_tabs[0])
        self.driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/div/div[1]/div/div[1]/div[1]/div/div/button/span[2]').click()
        clipboard_text = pyperclip.paste()
        self.addresses.append(clipboard_text)
        time.sleep(SHORT_WAIT_TIME)

    def work(self):
        self.addresses = []
        self.open_browser()
        self.driver.implicitly_wait(3)
        self.metamask_controller.login(self.metamask_password)
        try:
            for i in range(2, MAX):
                self.append_account_address_list(i)
        except Exception as e:
            print(e)
            print(f"계정 {i} 까지 진행되다 중단되었습니다.")
            pprint.pprint(self.addresses)
            return
        print("진행 완료")
        pprint.pprint(self.addresses)

if __name__ == "__main__":
    metamask_account_generator = MetamaskAccountGenerator()
    metamask_account_generator.work()


