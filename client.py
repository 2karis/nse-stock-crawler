from ticker_data import ticker_data
from market_data import market_data
import pytz
import time as tt
from datetime import datetime, timedelta, date, time
import json

#check if its a weekday
def is_week_day():
    return datetime.today().weekday() < 5

#check if it's correct time
def is_in_time():
    tz = pytz.timezone('Africa/Nairobi')
    nairobi_now = datetime.now(tz).time()
    nairobi_hour = nairobi_now.hour
    nairobi_minute = nairobi_now.minute
    set_time = time(15, 31)
    time_hour = set_time.hour
    time_minute = set_time.minute

    if nairobi_hour == time_hour and nairobi_minute == time_minute:
        return 1
    return 0




print("crawler active")
while 1:
    #if its weekday and correct time then crawl site
    if is_week_day() and is_in_time():
        f = open('config.json')
        #load configuration file
        config = json.load(f)
        t = ticker_data(config)
        m = market_data(config)
        collected = 0
        for s in (m, t):
            s.login()
            collected = s.crawl_data()
            print(collected)
        if collected == 1:
            print("[",datetime.now()," ] info collected  ")
            print()

            tt.sleep(300)
        else:
            print("[", datetime.now(), " ] failed ")
            print()
