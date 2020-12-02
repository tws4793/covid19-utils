import requests
import pandas as pd
from datetime import date
from bs4 import BeautifulSoup

def get_request(url: str):
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'
    }
    print(url)

    response = requests.get(url, headers = header)
    
    return response

def get_content_soup(url: str) -> BeautifulSoup:
    response = get_request(url)
    
    assert response.status_code == 200, 'Content not found'
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    return soup

def poll_gov_long_url(url: str, delay: int = 30, verbose: bool = False):
    response = get_request(url)

    if (response.status_code == 200):
        return response
    else:
        return poll_gov_long_url(url, delay, verbose)

# def poll_long_url(url_short, delay = 30, verbose = False):
#     status_code = 0
#     long_url = ''

#     try:
#         while(status_code != 200):
#             response = get_request(url_short)
#             status_code = response.status_code
#             long_url = response.url

#             if verbose:
#                 print('Not released yet')

#             time.sleep(delay)
        
#         if verbose:
#             print('Released')
#     except Exception:
#         pass
#     finally:
#         return long_url

def get_gov_short_url(path: str, include_protocol: bool = True) -> str:

    url_short_gov = ('https://' if include_protocol else '') + 'go.gov.sg/'
    url_short = url_short_gov + path

    return url_short

def get_gov_long_url(path: str) -> str:
    '''
    Get the long URL from the path.
    '''
    try:
        url_short = get_gov_short_url(path)
        
        soup = get_content_soup(url_short)
        url_long = str(soup.find('p').get('data-href'))

        return url_long
    except Exception as e:
        print('Error: ', e)

        return ''

def get_moh_long_url_predefined(n_new: int, n_discharged: int) -> str:
    return 'https://www.moh.gov.sg/news-highlights/details/' + \
        str(n_discharged) + '-more-cases-discharged-' + \
        str(n_new) + '-new-cases-of-covid-19-infection-confirmed'

def get_moh_annexe_urls(url: str):
    try:
        soup = get_content_soup(url)
        links = soup.find(id = 'widgetDetailsContentBlock').find_all('a', href = True)
        urls = [l['href'] for l in links][-2:]

        return urls

        # return {
        #     'annex_clusters': urls[0],
        #     'annex_cases': urls[1]
        # }
    except Exception as e:
        print('Error: ', e)

        return list(range(2))

def generate_initial_list(start = '2020-02-07', end = date.today()):
    dates = pd.date_range(start, end, freq = 'D')

    df = pd.DataFrame({'date': dates})
    df['url_short'] = 'moh' + df['date'].dt.strftime('%-d%b').str.lower()

    return df
