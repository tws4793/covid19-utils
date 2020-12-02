import emoji
import pyperclip
from datetime import date
from .date import get_date_parameter
from .url import get_gov_short_url, get_gov_long_url
from typing import Tuple

def extended(
    report_date = date.today(),
    url_short: str = '',
    url_long: str = '',
    cases = {},
    recovered = {},
    deaths = {},
    stable = {},
    critical = {},
):
    '''
    Format (new, total)

    '''
    date_parameter = get_date_parameter(report_date)
    url_short = get_gov_short_url(date_parameter)
    url_long = get_gov_long_url(date_parameter)
    
    # fig = lambda i, j: str(i) + ' (' + ('%+d' % j if j != 0 else '-') + ')'
    fig = lambda t: str(t['total']) + ' (' + ('%+d' % t['new'] if t['new'] != 0 else '-') + ')'

    closed = {
        'new': recovered['new'] + deaths['new'],
        'total': recovered['total'] + deaths['total']
    }

    active = {
        'new': stable['new'] + critical['new'],
        'total': stable['total'] + critical['total']
    }

    message = [
        'COVID-19 Update as of ' + report_date.strftime('%-d %b %Y') +', 1200 hrs:',
        '',
        'Total: ' + fig(cases),
        '',
        'Closed: ' + fig(closed),
        '- Discharged: ' + fig(recovered),
        '- Deaths: ' + fig(deaths),
        '',
        'Active: ' + fig(active),
        '- Stable: ' + fig(stable),
        '- Critical: ' + fig(critical),
        '',
        url_short,
        url_long
    ]
    
    return message

def summarised(
    report_date = date.today(),
    url_short: str = '',
    url_long: str = '',
    cases = {},
    recovered = {},
):
    '''
    Parameters:
        url_short (str)
    Returns:
        list of str: Each line of the report
    '''
    date_parameter = get_date_parameter(report_date)
    url_short = get_gov_short_url(date_parameter)
    url_long = get_gov_long_url(date_parameter)

    message = [
        emoji.emojize(':Singapore:') + ' ' + str(recovered['new']) + ' / ' + str(cases['new']),
        str(recovered['total']) + ' / ' + str(cases['total']) + \
            ' (' + '{:.2%}'.format(recovered['percent']) + ')',
        '',
        url_short,
        url_long
    ]
    return message

def generate(message):
    '''
    Copy the report to the clipboard and print the report from the message.
    '''

    try:
        report = '\n'.join(message)
        pyperclip.copy(report)
    except Exception:
        pass
    finally:
        print(report)
