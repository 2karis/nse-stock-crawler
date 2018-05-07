import time
import datetime
from ticker_data import ticker_data
from market_data import market_data

username = ""
password = ""

t = ticker_data(username,password)
m = market_data(username,password)
while 1:
	for s in (t, m):
		s.db_connection()
		print('logging in..')
		s.login()
		print('collecting ticker..')
		s.crawl_data()
		s.db_close()
		del s
		print()
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	print('time collected :', st)
	# this makes the program wait 15 minutes before each crawl
	time.sleep(900)

