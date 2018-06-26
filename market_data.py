from scrapper import scrapper
from bs4 import BeautifulSoup
import re
import time


class market_data(scrapper):
    def __init__(self, c):
        super().__init__(c)
        print("market scapper initialized")

        
    def crawl_data(self):
        self.browser.open('https://onlinetrading.nse.co.ke/tradeweb111/MarketDetails.aspx?wl=Default')
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
        sql = "INSERT INTO market(security, last_price, demand_qty, demand_price, supply_price, supply_qty, last_qty, high, low) VALUES "
        for row in sdarr:
            sub_row = [row[2], row[8], row[9], row[10], row[11], row[12]]
            high_low = self.sortlist(sub_row)
            sql = sql + "( '"+row[0]+"', "+ row[2]+", "+row[5]+", "+row[6]+", "+row[8]+", "+row[7]+", "+row[4]+", "+max(high_low)+", "+min(high_low)+"),"
        sql = sql[:-1] + ";"    
        self.db_query(sql)

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
    
