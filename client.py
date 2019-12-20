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
def is_in_time(hour, minute):
    tz = pytz.timezone('Africa/Nairobi')
    nairobi_now = datetime.now(tz).time()
    nairobi_hour = nairobi_now.hour
    nairobi_minute = nairobi_now.minute
    set_time = time(int(hour), int(minute))
    time_hour = set_time.hour
    time_minute = set_time.minute

    if nairobi_hour == time_hour and nairobi_minute == time_minute:
        return 1
    return 0




print("crawler active")

#if 1:
while 1:
    f = open('config.json')
    config = json.load(f)
    f.close()
    hour = int(config["hour"])
    minute = int(config["minute"])
    #if 1:
    if is_week_day() and is_in_time(hour,minute):
        market = market_data(config)
        page = market.fetch_data()
        arr = market.clean_data(page)
        sdarr = market.organize_data(arr)
        collected = 0
        market.post_data(sdarr)
        tt.sleep(config["sleep"])


        print(collected)
        if collected == 1:
            print("[",datetime.now()," ] info collected  ")
            print()


        else:
            print("[", datetime.now(), " ] failed ")
            print()
