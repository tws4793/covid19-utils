import time
from datetime import date

def get_date(date = date.today()):
    today_format = date.strftime('%-d %b %Y')
    today_url = 'go.gov.sg/moh' + date.strftime('%-d%b').lower()

    return today_format, today_url
