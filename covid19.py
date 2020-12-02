from utils import manual, date, terminal, url, report
from datetime import date

def main():
    args = terminal.arguments().parse_args()
    if(args.debug):
        print(str(args))
    # manual.report_v1(date.get_date_head(), date.get_date_url(), True, 'covid19.txt')

    info = manual.report_v2(vars(args), debug = args.debug)
    report_message = report.summarised(
        report_date = date.today(),
        cases = info['cases'],
        recovered = info['recovered']
    )
    # report2 = manual.report_v3(recovered = args.total_recovered)
    report.generate(report_message)

if __name__ == '__main__':
    main()
