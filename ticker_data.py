from scrapper import scrapper
from bs4 import BeautifulSoup
import re
import time


class ticker_data(scrapper):
    def __init__(self, c):
        super().__init__(c)
        print("ticker scapper initialized")

        
    def crawl_data(self):
        self.browser.open(self.config['brokerage']['ticker'])
        page = self.browser.get_current_page()
        soup = BeautifulSoup(str(page), 'lxml')
        if(soup.find("div", {"class": "CSPLTickerContainer"})):
            div = soup.find("div", {"class": "CSPLTickerContainer"})
            ul =  div.find("ul")
            li =  ul.find("li")
            tickers=[]

            for li in ul:
                combo = li.text.split('|', 1)[0]
                security_price, change = combo.split(' ')
                security = re.split('(\d+)',security_price)
                price = ''.join(security[1:4])
                #items.append([security[0] ,price , change])
                tickers.append({'security': security[0], 'price': price, 'price_change': change})

            print("posting to : ", self.config['brokerage']['post_ticker'])

            self.api_post(self.config['brokerage']['post_ticker'], tickers)
            print("ticker data collected")

            return 1
        return 0



