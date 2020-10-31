import emoji
import pyperclip
import requests
import time
import yaml
import pandas as pd
from .date import *
from .url import *

def calculate_n_recovered(today: int, previous: int) -> int:
    assert today >= previous, 'Today\'s recovered figure must be equal to or higher than yesterday!'
    return today - previous

def calculate_p_recovered(recovered: int, total: int) -> float:
    assert recovered <= total, 'Recovered figure must be less than total figure!'
    return recovered / total

def write_to_file(file, total, discharged, deaths, critical):
    report = '\n'.join([str(total), str(discharged), str(deaths), str(critical)])

    with open(file, 'w') as f:
        f.write(report)

def report_v1(date_today_format, today_url, debug = False, file = 'covid19.txt'):
    # Get New Figures
    new_total = int(input('New Cases: '))
    new_discharged = int(input('New Discharged: '))
    new_deaths = int(input('New Deaths: '))
    new_closed = new_discharged + new_deaths
    new_active = new_total - new_closed
    critical = int(input('Current Critical: '))

    # Get Previous Day Figures
    with open(file, 'r') as f:
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
    with open(file[:-4] + ('.bak' if debug else '') + file[-4:], 'w') as f:
        f.write(str(total) \
            + '\n' + str(discharged)
            + '\n' + str(deaths)
            + '\n' + str(critical))

    fig = lambda i, j: str(i) + ' (' + ('%+d' % j if j != 0 else '-') + ')'

    message = [
        'COVID-19 Update as of ' + date_today_format +', 1200 hrs:',
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

    return message

def report_v2(debug: bool = False, file: str = 'covid19.txt', **kwargs):
    # Get short and URL
    date_parameter = get_date_parameter()
    url_short = get_gov_short_url(date_parameter)
    url_long = get_gov_long_url(date_parameter)

    # This chunk to a separate portion
    with open(file, 'r') as f:
        previous_total = int(f.readline())
        previous_recovered = int(f.readline())

    new = int(input('New Cases: '))
    today = new + previous_total
    recovered = int(input('Today Recovered: '))

    if not(debug):
        write_to_file(file, today, recovered, 28, 0)

    return output_report_v2(
        url_short = url_short,
        url_long = url_long,
        new_recovered = calculate_n_recovered(recovered, previous_recovered),
        new_cases = new,
        total_recovered = recovered,
        total_cases = today,
        percent_recovered = calculate_p_recovered(recovered, today)
    )

def report_v3(**kwargs):
    '''
    For now assume night only update
    '''

    # Read latest figures
    df = read_figures()
    latest = df.iloc[-1]

    recovered = kwargs['recovered'] \
        if 'recovered' in kwargs \
            else latest['total_recovered']

    # Get short and URL
    date_parameter = get_date_parameter()
    url_short = get_gov_short_url(date_parameter)
    url_long = get_gov_long_url(url_short)

    # Calculate
    n_recovered = calculate_n_recovered(recovered, latest['total_recovered'])
    p_recovered = calculate_p_recovered(recovered, latest['total_cases'])

    return output_report_v2(
        url_short = url_short,
        url_long = url_long,
        new_recovered = n_recovered,
        new_cases = latest['new_cases'],
        total_recovered = recovered,
        total_cases = latest['total_cases'],
        percent_recovered = p_recovered
    )

def output_report_v2(url_short: str = '', url_long: str = '', **kwargs):
    '''
    Parameters:
        url_short (str)
    Returns:
        list of str: Each line of the report
    '''
    message = [
        str(kwargs['new_recovered']) + ' / ' + str(kwargs['new_cases']),
        str(kwargs['total_recovered']) + ' / ' + str(kwargs['total_cases']) + \
            ' (' + '{:.2%}'.format(kwargs['percent_recovered']) + ')',
        '',
        url_short,
        url_long
    ]
    return message

def read_figures():
    df = pd.read_csv('data/sandbox/figures.csv')
    df['date'] = pd.to_datetime(df['date'])

    return df

def read_latest_figures(df):
    return df.iloc[-1]

def generate_report(message):
    '''
    Copy the report to the clipboard and print the report from the message.
    '''

    try:
        report = '\n'.join(message)
        pyperclip.copy(report)
    except pyperclip.PyperclipException:
        pass
    except Exception:
        pass
    finally:
        print(report)
