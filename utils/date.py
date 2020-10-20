from datetime import date

def get_date_head(date = date.today()):
    return date.strftime('%-d %b %Y')

def get_date_url(date = date.today(), include_protocol = True):
    return ('https://' if include_protocol else '') +\
        'go.gov.sg/moh' + date.strftime('%-d%b').lower()
