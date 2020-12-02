import requests
import time
import yaml
import pandas as pd
from .date import *
from .url import *
from datetime import date

def calculate_figures(previous: int, new_figure = None, total = None):
    '''
    Parameters:
        previous
    Returns:
        list of str: Each line of the report
    '''

    assert type(new_figure) != type(
        total), 'Either new or total value must be entered!'

    # figure_assertion = lambda x: assert x != None and isinstance(x, int), 'Figure must be an integer!'
    figures = {
        'new': int(new_figure) if new_figure != None else total - previous,
        'total': int(total) if total != None else previous + new_figure
    }

    return figures


def calculate_n_recovered(today: int, previous: int) -> int:
    assert today >= previous, 'Today\'s recovered figure must be equal to or higher than yesterday!'
    return today - previous

def calculate_p_recovered(recovered: int, total: int) -> float:
    assert recovered <= total, 'Recovered figure must be less than total figure!'
    return recovered / total

def write_to_file(file, total, discharged, deaths, critical):
    report = '\n'.join([str(total), str(discharged),
                        str(deaths), str(critical)])

    with open(file, 'w') as f:
        f.write(report)

def report_v1(date_today_format, today_url, debug: bool = False, file: str = 'covid19.txt'):
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
    if not(debug):
        write_to_file(file, total, discharged, deaths, critical)

    return {
        'new_cases': new_total,
        'total_cases': total,
        'new_recovered': new_discharged,
        'total_recovered': discharged,
        'new_deaths': new_deaths,
        'total_deaths': deaths,
        'new_stable': new_stable,
        'total_stable': stable,
        'new_critical': new_critical,
        'total_critical': critical
    }

def report_v2(arguments, debug: bool = False, file: str = 'covid19.txt'):
    # Get short and URL
    # date_parameter = get_date_parameter()
    # url_short = get_gov_short_url(date_parameter)
    # url_long = get_gov_long_url(date_parameter)

    # This chunk to a separate portion
    with open(file, 'r') as f:
        previous_total = int(f.readline())
        previous_recovered = int(f.readline())
        previous_deaths = int(f.readline())
        previous_critical = int(f.readline())

    new = int(arguments['new_cases'])
    today = new + previous_total
    recovered = int(arguments['total_recovered'])
    deaths = previous_deaths + int(arguments['new_deaths'])
    critical = int(arguments['total_icu'])

    if not(debug):
        write_to_file(file, today, recovered, deaths, critical)

    return {
        # 'url_short': url_short,
        # 'url_long': url_long,
        'cases': {
            'new': new,
            'total': today
        },
        'recovered': {
            'new': calculate_n_recovered(recovered, previous_recovered),
            'total': recovered,
            'percent': calculate_p_recovered(recovered, today)
        }
    }

def read_figures():
    df = pd.read_csv('data/sandbox/figures.csv')
    df['date'] = pd.to_datetime(df['date'])

    return df

def get_latest_figures(figures, df):
    df.at[0, ''] = 0

def update_figures(**kwargs):
    df = read_figures()
    latest = df.tail(1)

    # Read
    if(latest['date'] == date.today()):
        # Update
        pass
    else:
        # Insert

        # Read yesterday's figures
        df_new = latest.copy()

        # Update

        # Append
        df.append(df_new)

    # Save table
    df.to_csv('data/sandbox/figures.csv')

def read_latest_figures(df):
    return df.iloc[-1]
