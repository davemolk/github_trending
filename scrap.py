from datetime import datetime
from urllib.parse import urljoin
from parso import parse
import requests
from bs4 import BeautifulSoup

url = 'https://github.com/kestra-io/kestra'
base_url = 'https://github.com/'

def safe_get(soup, selector, attr):
    try:
        attribute = soup.select(f'{selector}')[0].text
    except AttributeError:
        return "Attribute missing"
    else:
        return attribute

def parse(url):
    headers = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    }
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

    print(name)
    print(description)
    print(language)
    print(total_stars)
    print(issues)
    print(pr)
    # try:
    #     name = soup.strong.a.text
    # except AttributeError:
    #     name = "Attribute missing"
    # try:
    #     url = urljoin(base_url, soup.strong.a['href'])
    # except AttributeError:
    #     url = "Attribute missing"
    # try:
    #     description = soup.find('p', class_='f4').text.strip()
    # except AttributeError:
    #     description = "Attribute missing"
    # try:
    #     language = soup.select_one('li.d-inline a span').text
    # except AttributeError:
    #     language = "Attribute missing"
    # try:
    #     total_stars = soup.find(id='repo-stars-counter-star').text
    # except AttributeError:
    #     total_stars = "Attribute missing"
    # try:
    #     issues = soup.find(id='issues-repo-tab-count').text
    # except AttributeError:
    #     issues = "Attribute missing"
    # try:
    #     pr = soup.find(id='pull-requests-repo-tab-count').text
    # except AttributeError:
    #     pr = "Attribute missing"

    # coders = soup.select('div.Layout-sidebar ul.list-style-none li.mb-2 a')
    # # print('coders', coders)
    # if coders != []:
    #     contributors = []
    #     for a in coders: 
    #         # print("type***************************", type(a['href']))
    #         # print(a['href'])
    #         if a['href'] != "":
    #             contributors.append(a['href'])
    #         else:
    #             contributors.append(url)
    # else:
    #     contributors = [url]

    # item = {
    #     'name': name,
    #     'url': url,
    #     'description': description,
    #     "language": language,
    #     "total_stars": total_stars,
    #     "issues": issues,
    #     "pr": pr,
    #     "contributors": contributors,
    #     "date": datetime.now(),
    # }

    # return item

parse(url)