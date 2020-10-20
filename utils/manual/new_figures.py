import emoji
import pyperclip
import requests

def calc(recovered, previous, today):
    n_recovered = recovered - previous
    pct_recovered = recovered / today

    return n_recovered, pct_recovered

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

def get_long_url_predefined(n_new, n_discharged):
    return 'https://www.moh.gov.sg/news-highlights/details/' + \
        str(n_discharged) + '-more-cases-discharged-' + \
        str(n_new) + '-new-cases-of-covid-19-infection-confirmed'

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
    with open(file, 'r') as f:
        previous_total = int(f.readline())
        previous_recovered = int(f.readline())

    new = int(input('New Cases: '))
    today = new + previous_total
    recovered = int(input('Today Recovered: '))

    if recovered < previous_recovered:
        raise Exception('Recovered figure should be higher than previous recovered figure!')

    calculated = calc(recovered, previous_recovered, today)
    singapore_flag = emoji.emojize(':singapore:')

    report = str(calculated[0]) + ' / ' + str(new) + '\n' + \
        str(recovered) + ' / ' + str(today) + ' (' + '{:.2%}'.format(calculated[1]) + ')' + '\n\n' + \
        today_url + get_long_url(today_url)
    
    try:
        pyperclip.copy(report)
    except pyperclip.PyperclipException:
        pass

    if not(debug):
        with open(file, 'w') as f:
            f.write(str(today) +\
                '\n' + str(recovered))

    print(report)
