import requests
import sys
import time
from utils.manual import new_figures
from utils.date import get_date_head, get_date_url

DEBUG = False
DELAY = 30
FILE = 'covid19.txt'
VERBOSE = True

# Get Today's Date
today_format = get_date_head()
today_url = get_date_url()

try:
    req = new_figures.get_request(today_url)

    print(today_url)
    while (req.status_code != 200):
        req = new_figures.get_request(today_url)
        if VERBOSE:
            print('Not released yet!')
        time.sleep(DELAY)

    if VERBOSE:
        print('Released!')
except KeyboardInterrupt:
    pass
finally:
    new_figures.report_v1(today_format, today_url, True, FILE)
