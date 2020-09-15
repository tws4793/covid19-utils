import requests
import sys
import time
from datetime import date
from utils.manual import new_figures

DEBUG = False
DELAY = 30
FILE = 'covid19.txt'
VERBOSE = True

# Get Today's Date
today = date.today()
today_format = today.strftime('%-d %b %Y')
today_url = 'go.gov.sg/moh' + today.strftime('%-d%b').lower()

try:
    path = 'https://' + today_url
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'
    }
    req = requests.get(path, headers = header)

    print(today_url)
    while (req.status_code != 200):
        req = requests.get(path)
        if VERBOSE:
            print('Not released yet!')
        time.sleep(DELAY)

    if VERBOSE:
        print('Released!')
except KeyboardInterrupt:
    pass
finally:
    new_figures.out_new_figures(today_format, today_url, True, FILE)
