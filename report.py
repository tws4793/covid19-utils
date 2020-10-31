from utils import manual, date, terminal, url

def main():
    args = terminal.arguments().parse_args()
    print(str(args))
    # manual.report_v1(date.get_date_head(), date.get_date_url(), True, 'covid19.txt')

    report = manual.report_v2(debug = args.debug)
    report = manual.report_v2(date.get_date_url(), debug = args.d)
    manual.generate_report(report)

if __name__ == '__main__':
    main()
