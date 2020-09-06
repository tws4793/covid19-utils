import requests
import sys
import time
from datetime import date

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
    # Get New Figures
    new_total = int(input('New Cases: '))
    new_discharged = int(input('New Discharged: '))
    new_deaths = int(input('New Deaths: '))
    new_closed = new_discharged + new_deaths
    new_active = new_total - new_closed
    critical = int(input('Current Critical: '))

    # Get Previous Day Figures
    with open(FILE, 'r') as f:
        total = int(f.readline())
        discharged = int(f.readline())
        deaths = int(f.readline())
        closed = discharged + deaths
        active = total - closed
        old_critical = int(f.readline())
        stable = active - old_critical

    # Update
    total += new_total
    closed += new_closed
    discharged += new_discharged
    deaths += new_deaths
    active += new_active
    new_critical = critical - old_critical
    stable = active - critical
    new_stable = new_active - new_critical

    # Write to file
    with open(FILE[:-4] + ('.bak' if DEBUG else '') + FILE[-4:], 'w') as f:
        f.write(str(total) \
            + '\n' + str(discharged)
            + '\n' + str(deaths)
            + '\n' + str(critical))

    fig = lambda i, j: str(i) + ' (' + ('%+d' % j if j != 0 else '-') + ')'

    message = [
        'COVID-19 Update as of ' + today_format +', 1200 hrs:',
        '',
        'Total: ' + fig(total, new_total),
        '',
        'Closed: ' + fig(closed, new_closed),
        '- Discharged: ' + fig(discharged, new_discharged),
        '- Deaths: ' + fig(deaths, new_deaths),
        '',
        'Active: ' + fig(active, new_active),
        '- Stable: ' + fig(stable, new_stable),
        '- Critical: ' + fig(critical, new_critical),
        '',
        today_url
        ]

    print()
    for m in message:
        print(m)