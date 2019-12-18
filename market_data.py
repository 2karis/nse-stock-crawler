from bs4 import BeautifulSoup
import mechanicalsoup
import random
import string
import requests
import json

import re
import time


class market_data():

    def __init__(self, config):
        self.config = config

        print("market scapper initialized")

        self.browser = mechanicalsoup.StatefulBrowser()

    def fetch_data(self):

        self.browser.open(self.config['login'])
        self.browser.select_form(nr=0)

        # User credentials
        self.browser['txtLogin'] = self.config['username']
        self.browser['txtPassword'] = self.config['password']

        # Login
        self.browser.submit_selected()

        self.browser.open(self.config['market'])
        page = self.browser.get_current_page()
        return page

    def clean_data(self, page):

        soup = BeautifulSoup(str(page), 'lxml')
        script = soup.find_all("script")
        jss = str(script[22])
        str_replace_qoutes = jss.replace('\"', '\\"')
        str_minus_semi_colon = str_replace_qoutes.replace(";", " ")
        str_minus_sdarr = str_minus_semi_colon.replace("sDArr", "")
        str_minus_equal = str_minus_sdarr.replace("=", "")

        # everything before sdarr
        head, sep, tail = str_minus_equal.partition('(jsiScripsInMW,50) ')
        # everything after sdarr
        head2, sep2, tail2 = tail.partition('  jsiMWrefreshDelay')
        result = re.sub("[\(\[].*?[\)\]]", "", head2)
        arr = result.split("' '")
        arr[0] = arr[0].replace("\'", "")
        arr[-1] = arr[-1].replace("\'", "")
        return arr



    def organize_data(self, arr):
        sdarr = []
        security_ = ""
        open_ = ""
        high_ = ""
        change_ = ""
        close_ = ""
        low_ = ""
        ltt_ = ""
        volume_ = ""
        turn_over_ = ""
        count = 0
        for i in range(len(arr)):
            count += 1

            if count == 1:  # good
                security_ = arr[i]

            if count == 10:  # good
                open_ = arr[i]

            if count == 11:  # good
                high_ = arr[i]

            if count == 3:
                change_ = arr[i]

            if count == 13:  # good
                close_ = arr[i]

            if count == 12:  # good
                low_ = arr[i]

            if count == 4:  # good
                ltt_ = arr[i]

            if count == 20:  # good
                volume_ = arr[i]

            if count == 19:  # good
                turn_over_ = arr[i]

            if count == 21:
                count = 0
                sdarr.append({
                    "security": security_,
                    "price_open": open_,
                    "price_high": high_,
                    "price_change": change_,
                    "price_low": low_,
                    "price_close": close_,
                    "last_trade": ltt_,
                    "volume": volume_,
                    "turn_over": turn_over_
                })
        return sdarr

    def post_data(self, sdarr):
        print("posting to : ", self.config['post_market'])
        r = requests.post(self.config['post_market'], data=json.dumps(sdarr))
        print(r)
        print("market data collected")



    def change_password(self):
        print('change pass')

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