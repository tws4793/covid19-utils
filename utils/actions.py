# import report, manual
from .url import generate_initial_list, get_gov_long_url

def generate_list():
    df = generate_initial_list()
    df['url_long'] = df['url_short'].apply(get_gov_long_url)
    df.to_csv('urls.csv')

def generate_report(args):
    pass