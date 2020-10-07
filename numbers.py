import pyperclip
import emoji
from utils.date import get_date

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
    singapore_flag = emoji.emojize(':singapore:')

    report = str(calculated[0]) + ' / ' + str(new) + '\n' + \
        str(recovered) + ' / ' + str(today) + ' (' + '{:.2%}'.format(calculated[1]) + ')' + '\n\n' + \
        'https://' + get_date()[1] + '\n' + \
        'https://www.moh.gov.sg/news-highlights/details/' + str(calculated[0]) + '-more-cases-discharged-' + str(new) + '-new-cases-of-covid-19-infection-confirmed'
    
    try:
        pyperclip.copy(report)
    except pyperclip.PyperclipException as e:
        pass

    print(report)