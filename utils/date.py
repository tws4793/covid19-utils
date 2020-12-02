from datetime import date

def get_date_parameter(date = date.today()):
    return 'moh' + date.strftime('%-d%b').lower()

def get_date_url(date = date.today(), include_protocol = True):
    return ('https://' if include_protocol else '') +\
        'go.gov.sg/' + get_date_parameter(date)
