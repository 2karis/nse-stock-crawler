import mechanicalsoup
from bs4 import BeautifulSoup
import re

browser = mechanicalsoup.StatefulBrowser()
browser.open("https://onlinetrading.ncbagroup.com/tradeweb/login.aspx")

browser.select_form(nr=0)

# User credentials
browser['txtLogin'] = 'kariukiigitau'
browser['txtPassword'] = 'nove1236'

# Login
browser.submit_selected()

browser.open('https://onlinetrading.ncbagroup.com/tradeweb/MarketDetails.aspx?wl=Default')
page = browser.get_current_page()

soup = BeautifulSoup(str(page), 'lxml')
script = soup.find_all("script")

jss =  str(script[22])
str_replace_qoutes = jss.replace('\"', '\\"')
str_minus_semi_colon = str_replace_qoutes.replace(";"," ")
str_minus_sdarr = str_minus_semi_colon.replace("sDArr","")
str_minus_equal = str_minus_sdarr.replace("=","")


head, sep, tail = str_minus_equal.partition('(jsiScripsInMW,50) ')

head2, sep2, tail2 = tail.partition('  jsiMWrefreshDelay')
result = re.sub("[\(\[].*?[\)\]]", "", head2)
arr = result.split("' '")
arr[0] = arr[0].replace("\'","")
arr[-1] = arr[-1].replace("\'","")

sdarr = []
sec = []
security_ = ""
open_ = ""
high_ = ""
change_ = ""
close_ = ""
low_ = ""
LTT_ = ""
volume_ = ""
turn_over_ = ""
count = 0
for i in range(len(arr)):
    count += 1

    if count == 1:
        security_ = arr[i]

    elif count == 10:
        open_ = arr[i]

    elif count == 11:
        high_ = arr[i]

    elif count == 3:
        change_ = arr[i]

    elif count == 13:
        close_ = arr[i]

    elif count == 12:
        low_ = arr[i]

    elif count == 4:
        LTT_ = arr[i]

    elif count == 20:
        volume_ = arr[i]

    elif count == 19:
        turn_over_ = arr[i]

    elif count == 21:
        count = 0
        sdarr.append({
            "security": security_,
            "open": open_,
            "high": high_,
            "change": change_,
            "close": close_,
            "low": low_,
            "LTT": LTT_,
            "volume": volume_,
            "turn_over": turn_over_
        })
        sec = []