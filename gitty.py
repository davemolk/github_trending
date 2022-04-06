from datetime import datetime
import logging
from time import sleep
from urllib.parse import urljoin
from urllib.request import Request
import requests
from bs4 import BeautifulSoup

logging.basicConfig(filename='gitty.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

language_count = {}
headers = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    }

def get_main():
    """
    Requests github.com/trending and calls the parse
    function on each repo found. Returns the repos object
    """
    base_url = 'https://github.com/'
    url = 'https://github.com/trending/'
    repos = {}

    try:
        r = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        logging.warning(f'Unable to get github.com/trending: {e}')
        return None
    soup = BeautifulSoup(r.text, 'html.parser')

    for repo in soup.find_all('article', class_='Box-row'):
        repo_url = urljoin(base_url, repo.h1.a['href'])
        logging.info(f"found these links: {repo_url}")
        item = parse(repo_url)
        repos[f"{item['name']}"] = item

    repos['language_count'] = language_count

    logging.info(f"returning {len(repos)} repos...now!")

    return repos

def safe_get(soup, selector, attr):
    """
    helper function: pass in a selector string, get an attribute
    """
    try:
        attribute = soup.select(f'{selector}')[0].text
    except AttributeError:
        logging.warning(f'unable to find <{selector}> for {attr} attribute')
        return "Attribute missing"
    else:
        return attribute

def parse(url):
    """
    Parse a given repo for desired information
    """
    try:
        r = requests.get(url, headers=headers)
    except requests.exceptions.RequestException:
            return None
    soup = BeautifulSoup(r.text, 'html.parser')

    name = safe_get(soup, 'strong a', 'name').replace('-', ' ')
    description = safe_get(soup, 'p.f4', 'description').strip()
    language = safe_get(soup, 'li.d-inline a span', 'language')
    total_stars = safe_get(soup, '#repo-stars-counter-star', 'total_stars')
    issues = safe_get(soup, '#issues-repo-tab-count', 'issues')
    pr = safe_get(soup, '#pull-requests-repo-tab-count', 'pr')
    url = url
    date = str(datetime.now())

    contributors = []
    
    

