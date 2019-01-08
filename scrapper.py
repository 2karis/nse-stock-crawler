import mechanicalsoup
from bs4 import BeautifulSoup
import random
import string
import requests
import json
import time as tt


class scrapper():
    def __init__(self, config):
        self.config = config
        self.browser = mechanicalsoup.StatefulBrowser()

    def login(self):
        self.browser.open(self.config['brokerage']['login'])
        self.browser.select_form(nr=0)
        self.browser['txtLogin'] = self.config['brokerage']['username']
        self.browser['txtPassword'] = self.config['brokerage']['password']
        self.browser.submit_selected()
        print("logging in")
        self.check_password()

    def logout(self):
        del self
        self.browser.follow_link()
        print("logged out")

    def api_post(self, link, data):
        r = requests.post(link, data=json.dumps(data))
        # r = 200
        print(r)

    def password_generator(self, size=8, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def write_password(self, password):
        self.config["brokerage"]["password"] = password

        with open("config.json", "w") as jsonFile:
            json.dump(self.config, jsonFile)

    def check_password(self):
        page = self.browser.get_current_page()
        soup = BeautifulSoup(str(page), 'lxml')
        # if this is the change password page
        if soup.title.text == '\r\n\tChange Password\r\n':
            # generate new password
            new_password = self.password_generator()
            # save to file
            self.write_password(new_password)
            self.browser.select_form(nr=0)
            self.browser['txtLoginID'] = self.config['brokerage']['username']
            self.browser['txtCurrPass'] = self.config['brokerage']['password']
            self.browser['txtNewPass'] = new_password
            self.browser['txtConfirmPass'] = new_password
            self.browser.submit_selected()
            print('password updated')
            # wait some seconds 10 seconds
            self.config = json.load(open('config.json'))
            tt.sleep(10)  # 900 86400
            self.login()