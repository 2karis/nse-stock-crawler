import mechanicalsoup
import MySQLdb
from bs4 import BeautifulSoup
import random
import string

class scrapper():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = browser = mechanicalsoup.StatefulBrowser()
        
    def login(self):
        self.browser.open("https://onlinetrading.nse.co.ke/tradeweb111/")
        self.browser.select_form(nr=0)
        self.browser['txtLogin'] = self.username
        self.browser['txtPassword'] = self.password
        self.browser.submit_selected()
        print("logging in")
        self.check_password()
        
    def logout(self):
        del self
        self.browser.follow_link()
        print("logged out")

    def db_query(self, sql):
        self.db = MySQLdb.connect(host="localhost",
                                  user="root",
                                  passwd="",
                                  db="oozacoke_scratch")
        print("database connection established")
        self.db.query(sql)
        self.db.commit()   
        print("data collected")
        self.db.close()
        print("closing connection")

    def password_generator(self, size=8, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def write_password(self, password):
        f = open("pass.txt", "w+")
        f.write(password)
        f.close()

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
            self.browser['txtLoginID'] = self.username
            self.browser['txtCurrPass'] = self.password
            self.browser['txtNewPass'] = new_password
            self.browser['txtConfirmPass'] = new_password
            self.browser.submit_selected()
            print('password updated')
            self.login()