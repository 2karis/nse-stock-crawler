import mechanicalsoup
from bs4 import BeautifulSoup
import random
import string
import requests
import json


class scrapper():
    def __init__(self, config):
        self.config = config
        self.browser = mechanicalsoup.StatefulBrowser()

    def login(self):
        self.browser.open(self.config['login'])
        self.browser.select_form(nr=0)
        self.browser['txtLogin'] = self.config['username']
        self.browser['txtPassword'] = self.config['password']
        self.browser.submit_selected()
        print("logging in")
        self.check_password()

    def logout(self):
        del self
        self.browser.follow_link()
        print("logged out")

    def api_post(self, link, data):
        #r = requests.post(link, data=json.dumps(data))
        #print(r)
        print(data)

    def password_generator(self, size=8, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def write_password(self, password):
        self.config["password"] = password

        with open("config.json", "w") as jsonFile:
            json.dump(self.config, jsonFile, indent=4, sort_keys=True)

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
            self.browser['txtLoginID'] = self.config['username']
            self.browser['txtCurrPass'] = self.config['password']
            self.browser['txtNewPass'] = new_password
            self.browser['txtConfirmPass'] = new_password
            self.browser.submit_selected()
            print('password updated to ', new_password)