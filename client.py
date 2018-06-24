from ticker_data import ticker_data
from market_data import market_data
import pytz
import time as tt
from datetime import datetime, timedelta, date, time


def getTimes():
    tz = pytz.timezone("Africa/Nairobi")
    the_date = date.today() 

    midnight_without_tzinfo = datetime.combine(the_date, time())
    midnight_with_tzinfo = tz.localize(midnight_without_tzinfo)
    midnight = midnight_with_tzinfo.astimezone(pytz.utc)
    start = midnight_without_tzinfo + timedelta(hours=17, minutes=0)

    end = midnight_without_tzinfo + timedelta(hours=17, minutes=30)
    now = datetime.now()
#     print(midnight_without_tzinfo)
#     print(midnight_with_tzinfo)
#     print(start)
#     print(end)
    return start, end, now


def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else: #Over midnight
        return nowTime >= startTime or nowTime <= endTime


def isWeekDay():
    return datetime.today().weekday()<5


startTime, endTime, nowTime = getTimes()


def try_stocks(start_time, end_time, now_time):
    #if isWeekDay() and isNowInTimePeriod(start_time, end_time, now_time):

    if isWeekDay():
        file = open('pass.txt', 'r')
        password = str(file.read())
        t = ticker_data('karis', password)
        m = market_data('karis', password)

        for s in (t, m):
            s.login()
            s.crawl_data()
            print()
        ts = tt.time()
        st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print('time collected :', st)
    else:
        print("bad time")
    tt.sleep(86400)#900
    now_time = datetime.now()
    print(start_time, end_time, now_time)
    try_stocks(start_time, end_time, now_time)


try_stocks(startTime, endTime, nowTime)