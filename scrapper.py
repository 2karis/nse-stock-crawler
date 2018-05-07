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
        self.db = MySQLdb.connect(host="localhost",
                                  user="root",
                                  passwd="",
                                  db="nse")
        '''
        'db'=> [
        'driver'=>'mysql',
        'host'=>'localhost',
        'database'=>'oozacoke_scratch',
        'username'=>'oozacoke_admin',/* oozacoke_admin */
        'password'=>'zCcnOhdZA8XS',/* zCcnOhdZA8XS */
        'collation'=>'utf_unicode_ci',
        'prefix'=>''
        '''
        print("database connection established")
        
    def db_query(self, sql):
        self.db.query(sql)
        self.db.commit()   
        print("data collected")
        
    def db_close(self):
        self.db.close()
        print("closing connection")
        
        
