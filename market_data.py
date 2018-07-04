from scrapper import scrapper
from bs4 import BeautifulSoup
import re
import time


class market_data(scrapper):
    def __init__(self, c):
        super().__init__(c)
        print("market scapper initialized")

        
    def crawl_data(self):
        self.browser.open(self.config['brokerage']['market'])
        page = self.browser.get_current_page()
        soup = BeautifulSoup(str(page), 'lxml')
        script = soup.find_all("script")
        
        jss =  str(script[22])
        str_replace_qoutes = jss.replace('\"', '\\"')
        str_minus_semi_colon = str_replace_qoutes.replace(";"," ")
        str_minus_sdarr = str_minus_semi_colon.replace("sDArr","")
        str_minus_equal = str_minus_sdarr.replace("=","")

        #everything before sdarr
        head, sep, tail = str_minus_equal.partition('(jsiScripsInMW,50) ')
        #everything after sdarr
        head2, sep2, tail2 = tail.partition('  jsiMWrefreshDelay')
        result = re.sub("[\(\[].*?[\)\]]", "", head2)
        arr = result.split("' '")
        arr[0] = arr[0].replace("\'","")
        arr[-1] = arr[-1].replace("\'","")
        
        sdarr = []
        sec = []
        count =1
        for i in range(len(arr)):
            count = count + 1
            sec.append(arr[i])
            if count ==22:
                count = 1
                sdarr.append(sec)
                sec =[]
        markets=[]
        for row in sdarr:
            sub_row = [row[2], row[8], row[9], row[10], row[11], row[12]]
            high_low = self.sortlist(sub_row)
            markets.append({"security": row[0],
                            "last_price": row[2],
                            "demand_qty": row[5],
                            "demand_price": row[6],
                            "supply_price": row[8],
                            "supply_qty": row[7],
                            "last_qty": row[4],
                            "high": max(high_low),
                            "low": min(high_low)
                            })
        print("posting to : ", self.config['brokerage']['post_market'])

        self.api_post(self.config['brokerage']['post_market'], markets)


        print("market data collected")

    def logout(self):
        del self
        self.browser.follow_link()
        print("logged out")
    def sortlist(self, mylist):
        newlist=[]
        for item in mylist:
            if float(item) > 0:
                newlist.append(item)

        if newlist == []:
            newlist = [str(0.00), str(0.00)]
        return newlist
    
