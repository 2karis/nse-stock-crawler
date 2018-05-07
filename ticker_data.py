from scrapper import scrapper
from bs4 import BeautifulSoup
import re
import time


class ticker_data(scrapper):
    def __init__(self, s,t):
        super().__init__(s,t)
        print("ticker scapper initialized")

        
    def crawl_data(self):
        self.browser.open("https://onlinetrading.nse.co.ke/tradeweb111/TWHome.aspx")
        page = self.browser.get_current_page()
        soup = BeautifulSoup(str(page), 'lxml')
        div = soup.find("div", {"class": "CSPLTickerContainer"})
        ul =  div.find("ul")
        li =  ul.find("li")
        sql = "INSERT INTO ticker (security, price, price_change) VALUES "
        for li in ul:
            combo = li.text.split('|', 1)[0]
            security_price, change = combo.split(' ')
            security = re.split('(\d+)',security_price)
            price = ''.join(security[1:4])
            #items.append([security[0] ,price , change])
            sql = sql + "('"+security[0]+"', "+ price+", "+change+"),"
        sql = sql[:-1] + ";"
        self.db_query(sql)
        
        print("ticker data collected")



