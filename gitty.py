from datetime import datetime
from time import sleep
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


language_count = {}
base_url = 'https://github.com/'

def get_main_page():
    headers = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    }
    url = 'https://github.com/trending/'
    try:
        r = requests.get(url, headers=headers)
    except requests.exceptions.RequestException:
            return None
    return BeautifulSoup(r.text, 'html.parser')

def get_links():
    soup = get_main_page()
    repo_list = []
    for repo in soup.find_all('article', class_='Box-row'):
        repo_url = urljoin(base_url, repo.h1.a['href'])
        repo_list.append(parse_repo(repo_url))
    
    return repo_list, language_count

# def safe_get(soup, selector):
#     try:
#         attribute = soup.select(selector)
#     except AttributeError:
#         attribute = "Attribute missing"
#     return attribute

def parse_repo(url):
    headers = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    }
    try:
        r = requests.get(url, headers=headers)
    except requests.exceptions.RequestException:
            return None
    soup = BeautifulSoup(r.text, 'html.parser')
    
    sleep(1)
    
    try:
        name = soup.strong.a.text
    except AttributeError:
        name = "Attribute missing"
    try:
        url = urljoin(base_url, soup.strong.a['href'])
    except AttributeError:
        url = "Attribute missing"
    try:
        description = soup.find('p', class_='f4').text.strip()
    except AttributeError:
        description = "Attribute missing"
    try:
        language = soup.select_one('li.d-inline a span').text
    except AttributeError:
        language = "Attribute missing"
    try:
        total_stars = soup.find(id='repo-stars-counter-star').text
    except AttributeError:
        total_stars = "Attribute missing"
    try:
        issues = soup.find(id='issues-repo-tab-count').text
    except AttributeError:
        issues = "Attribute missing"
    try:
        pr = soup.find(id='pull-requests-repo-tab-count').text
    except AttributeError:
        pr = "Attribute missing"

    coders = soup.select('div.Layout-sidebar ul.list-style-none li.mb-2 a')
    if coders != []:
        contributors = []
        for a in coders: 
            if a['href'] != "":
                contributors.append(a['href'])
            else:
                contributors.append(url)
    else:
        contributors = [url]

    if language != "Attribute missing":
        language_count[language] = 1 + language_count.get(language, 0)

    item = {
        'name': name,
        'url': url,
        'description': description,
        "language": language,
        "total_stars": total_stars,
        "issues": issues,
        "pr": pr,
        "contributors": contributors,
        "date": datetime.now(),
    }

    return item


print(get_links())
