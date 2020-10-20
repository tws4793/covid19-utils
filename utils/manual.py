import emoji
import pyperclip
import requests
import time

def calculate_n_recovered(today, previous):
    assert today >= previous, 'Today\'s recovered figure must be equal to or higher than yesterday!'
    return today - previous

def calculate_p_recovered(recovered, total):
    assert recovered <= total, 'Recovered figure must be less than total figure!'
    return recovered / total

def get_request(url_short):
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'
    }

    return requests.get(url_short, headers = header)

def get_long_url(url_short):
    try:
        response = get_request(url_short)
        status_code = response.status_code
        
        return '\n' + response.url if status_code == 200 else ''
    except Exception:
        return ''

def poll_long_url(url_short, delay = 30, verbose = False):
    status_code = 0
    long_url = ''

    try:
        while(status_code != 200):
            response = get_request(url_short)
            status_code = response.status_code
            long_url = response.url

            if verbose:
                print('Not released yet')

            time.sleep(delay)
        
        if verbose:
            print('Released')
    except Exception:
        pass
    finally:
        return long_url

def get_long_url_predefined(n_new, n_discharged):
    return 'https://www.moh.gov.sg/news-highlights/details/' + \
        str(n_discharged) + '-more-cases-discharged-' + \
        str(n_new) + '-new-cases-of-covid-19-infection-confirmed'

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

    print()
    for m in message:
        print(m)

def report_v2(today_url, debug = False, file = 'covid19-2.txt'):
    long_url = get_long_url(today_url)

    # This chunk to a separate portion
    with open(file, 'r') as f:
        previous_total = int(f.readline())
        previous_recovered = int(f.readline())

    new = int(input('New Cases: '))
    today = new + previous_total
    recovered = int(input('Today Recovered: '))

    if not(debug):
        write_to_file(file, today, recovered, 28, 0)
        # with open(file, 'w') as f:
        #     f.write(str(today) +\
        #         '\n' + str(recovered) +\
        #         '\n' + str(28) +\
        #         '\n' + str(0))

    # singapore_flag = emoji.emojize(':singapore:')

    message = [
        str(calculate_n_recovered(recovered, previous_recovered)) + ' / ' + str(new),
        str(recovered) + ' / ' + str(today) + ' (' + '{:.2%}'.format(calculate_p_recovered(recovered, today)) + ')',
        '',
        today_url + long_url
    ]

    return message

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
