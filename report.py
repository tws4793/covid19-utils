import argparse
from utils import manual, date

def arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-d',
        help = 'debug mode',
        action = 'store_true'
    )

    return parser.parse_args()

def main():
    # manual.poll_long_url(date.get_date_url(), verbose = True)

    args = arguments()
    print(str(args))
    # manual.report_v1(date.get_date_head(), date.get_date_url(), True, 'covid19.txt')
    report = manual.report_v2(date.get_date_url(), debug = args.d)
    manual.generate_report(report)

if __name__ == '__main__':
    main()
