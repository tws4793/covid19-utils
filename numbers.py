def calc(recovered, previous, today):
    n_recovered = recovered - previous
    pct_recovered = recovered / today

    return n_recovered, pct_recovered

if __name__ == '__main__':
    new = int(input('New Cases: '))
    today = int(input('No Cases Cumulative: '))
    previous = int(input('Previous Recovered: '))
    recovered = int(input('Today Recovered: '))

    calculated = calc(recovered, previous, today)

    report = str(calculated[0]) + ' / ' + str(new) + '\n' + \
        str(recovered) + ' / ' + str(today) + ' (' + '{:.2%}'.format(calculated[1]) + ')'
    
    print(report)