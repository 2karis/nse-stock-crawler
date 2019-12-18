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
f1 = open('config_dev.json')
config1 = json.load(f1)
f1.close()
hour = int(config1["hour"])
minute = int(config1["minute"])
while 1:
    #if 1:
    if is_week_day() and is_in_time(hour,minute):
        #if  is_in_time(hour,minute):
        #if is_week_day():
        f = open('config_dev.json')
        config = json.load(f)
        f.close()

        market = market_data(config)
        page = market.fetch_data()

        page = market.fetch_data()
        arr = market.clean_data(page)
        sdarr = market.organize_data(arr)

        market.post_data(sdarr)
        tt.sleep(config["sleep"])
        collected = 0

        print(collected)
        if collected == 1:
            print("[",datetime.now()," ] info collected  ")
            print()


        else:
            print("[", datetime.now(), " ] failed ")
            print()
