
def out_new_figures(date_today_format, today_url, debug = False, file = 'covid19.txt'):
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
