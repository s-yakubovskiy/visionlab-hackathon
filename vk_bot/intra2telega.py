#!python3.7

import bs4, sys, requests, os, logging
import time, schedule
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class IntraWatcher:

    def __init__(self, name='arau'):
        self.name = name
        self.signin = "https://signin.intra.42.fr/users/sign_in"
        self.intra_profile = "https://profile.intra.42.fr/users/" + self.name
        self.chrome_options = Options()
        self.driver = self.init_driver()
        self.login_site()
        self.soap = None
        self.response = None

    def login_site(self):
        self.driver.get(self.signin)
        self.driver.find_element_by_id("user_login").send_keys("yharwyn-")
        self.driver.find_element_by_id("user_password").send_keys("EvilS@L@mandra7")
        self.driver.find_element_by_class_name("btn-login").click()
        logger.info(self.signin)

    @staticmethod
    def telegram_sendtext(bot_message):
        bot_token = '899664750:AAEkC8JPCkoVHQ4f3yRuI4IAUoa-D8W5udI'
        bot_chatID = '499049359'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' \
                    + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
        return response.json()

    def init_driver(self):
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-gpu")
        logger.info("Initializing driver... complete")
        logger.info(self.chrome_options)
        return webdriver.Chrome(options=self.chrome_options)

    def get_person(self):
        logger.info(self.name)
        self.driver.get(self.intra_profile)
        content = self.driver.page_source
        self.soap = bs4.BeautifulSoup(content, "html.parser")
        arau_status = self.soap.find_all('div', attrs={'class': 'user-poste-status'})
        arau_location = self.soap.find_all('div', attrs={'class': 'user-poste-infos'})
        self.response = "This fag is '%s' at '%s'" % (arau_status[0].text.strip(), arau_location[0].text.strip())
        logger.info(self.response)


if __name__ == "__main__":
    arau = IntraWatcher("arau")
    arau.get_person()
    # IntraWatcher.telegram_sendtext(arau.response)

    arau.driver.quit()
