from ticker_data import ticker_data
from market_data import market_data
import pytz
import time as tt
from datetime import datetime, timedelta, date, time
import json


#
# def getTimes():
#     tz = pytz.timezone("Africa/Nairobi")
#     the_date = date.today()
#     midnight_without_tzinfo = datetime.combine(the_date, time())
#     midnight_with_tzinfo = tz.localize(midnight_without_tzinfo)
#     midnight = midnight_with_tzinfo.astimezone(pytz.utc)
#     start = midnight_without_tzinfo + timedelta(hours=17, minutes=0)
#     end = midnight_without_tzinfo + timedelta(hours=17, minutes=30)
#     now = datetime.now()
#     return start, end, now
#
#
# def isNowInTimePeriod(startTime, endTime, nowTime):
#     if startTime < endTime:
#         return nowTime >= startTime and nowTime <= endTime
#     else: #Over midnight
#         return nowTime >= startTime or nowTime <= endTime


def isWeekDay():
    return datetime.today().weekday() < 5


def is_in_time():
    tz = pytz.timezone('Africa/Nairobi')
    nairobi_now = datetime.now(tz).time()
    nairobi_hour = nairobi_now.hour
    nairobi_minute = nairobi_now.minute
    set_time = time(15, 35)
    time_hour = set_time.hour
    time_minute = set_time.minute

    if nairobi_hour == time_hour and nairobi_minute == time_minute:
        return 1
    return 0



def try_stocks():
    print("crawler active")
    #if isWeekDay() and isNowInTimePeriod(start_time, end_time, now_time):
    while 1:
        if isWeekDay() and is_in_time():
            f = open('config.json')
            config = json.load(f)
            t = ticker_data(config)
            m = market_data(config)
            collected =0
            for s in (m, t):
                s.login()
                collected = s.crawl_data()
                print(collected)
            if collected == 1:
                print("time collected : ", datetime.now())
                tt.sleep(300)#900 86400
    # now_time = datetime.now()
    # print(start_time, end_time, now_time)
    # try_stocks(start_time, end_time, now_time)



# startTime, endTime, nowTime = getTimes()

try_stocks()