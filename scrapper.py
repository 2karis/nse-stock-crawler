import mechanicalsoup
import MySQLdb

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
         
        
    def logout(self):
        del self
        self.browser.follow_link()
        print("logged out")
        
    def db_connection(self):
        self.db = MySQLdb.connect(host="my_host",
                                  user="my_user",
                                  passwd="my_password",
                                  db="my_database")
        
        print("database connection established")
        
    def db_query(self, sql):
        self.db.query(sql)
        self.db.commit()   
        print("data collected")
        
    def db_close(self):
        self.db.close()
        print("closing connection")
        
        
